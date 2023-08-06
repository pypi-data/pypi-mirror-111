import sys
import logging
import kamocli
import requests
import datetime
import dateutil
import json
import time
import copy
from time import sleep
import boto3
from urllib.parse import urlparse, urljoin
from io import BytesIO
from operator import attrgetter, itemgetter

from kamocli.utils import (
    dumps,
    abort,
    print_tab,
    fmt_date,
    check_tenant,
    print_table,
    get_tenant_url,
    success,
    find_regions,
    find_nodes,
    out,
    format_region_name,
    parse_region_name,
    get_builds_from_s3_url,
)
from kamosdk.exceptions import ServerError
from tabulate import tabulate

log = logging.getLogger(__name__)

from typer import Typer, Context, Argument, Option, echo, secho, confirm, style

app = Typer()


@app.callback(
    help="Manage jobs of UE4 server builds",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
@check_tenant
def cli(
    ctx: Context,
    is_all: bool = Option(False, "-a", "--all", is_flag=True, help="Manage all tenants at once"),
):
    ctx.obj.tenant = ctx.obj.session.profile.tenant
    ctx.obj.is_all = is_all


@app.command("list")
def list_jobs(
    ctx: Context,
    status: str = Option(
        "pending,processing,running,stopping",
        "-s",
        "--status",
        show_default=True,
        help="Status to filter for",
    ),
    is_all: bool = Option(False, "-a", "--all", is_flag=True, help="Show all jobs regardless of status"),
):
    """List server jobs"""
    tenant = ctx.obj.session.profile.tenant
    if ctx.obj.is_all:
        tenant = None
    if is_all:
        status = ""
    url = ctx.obj.session.knode_url + f"/jobs"
    resp = ctx.obj.session.get(
        url,
        params={
            "tenant": tenant,
            "start": 0,
            "end": 100,
            "status": status,
            "sort": "created",
            "reverse": True,
        },
    )
    resp.raise_for_status()
    if ctx.obj.output == "json":
        echo(dumps(resp.json()))
        return
    node_heartbeats = {r["node_id"]: None for r in resp.json()}
    for node_id in node_heartbeats.keys():
        url = ctx.obj.session.knode_url + f"/nodes/{node_id}"
        last_heartbeat = None
        try:
            node_resp = ctx.obj.session.get(url)
            last_heartbeat = node_resp.json()["modified_date"]
        except Exception:
            pass
        node_heartbeats[node_id] = last_heartbeat

    lst = []
    headers = [
        "ID",
        "Status",
        "Tenant",
        "Version",
        "Regions",
        "Node",
        "IP Address",
        "Created",
        "Updated",
        "Result",
        "Heartbeat",
    ]
    for job in resp.json():
        args = job["args"]
        regions = ""
        for a in args:
            if a.startswith("-regions"):
                regions = a.split("=")[-1]
        address = "N/A"
        if job.get("ip_address"):
            address = "{}:{}".format(job.get("ip_address"), job.get("port"))
        heartbeat = node_heartbeats.get(job["node_id"])
        if heartbeat:
            dt = dateutil.parser.parse(heartbeat)
            heartbeat_txt = fmt_date(heartbeat)
            if dt < datetime.datetime.utcnow() - datetime.timedelta(minutes=5):
                heartbeat_txt = style(heartbeat_txt, fg="red")
        else:
            heartbeat_txt = style("Node not found", fg="red")
        lst.append(
            [
                job["job_id"],
                job["status"],
                job["tenant"],
                job["version"],
                regions,
                job["node_id"],
                address,
                fmt_date(job["create_date"]),
                fmt_date(job["modified_date"]),
                job.get("result"),
                heartbeat_txt,
            ]
        )
    if tenant:
        echo("Active jobs for tenant " + style(tenant, bold=True) + ":")
    else:
        echo("Active jobs for all tenants:")
    echo(tabulate(lst, headers=headers))


@app.command("view")
def view_job(ctx: Context, job_id: str = Argument(..., help="Job ID to view")):
    """View details about a specific job"""
    url = ctx.obj.session.knode_url + f"/jobs/{job_id}"
    try:
        resp = ctx.obj.session.get(url)
    except ServerError as ex:
        abort(ex)
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return

    for key, val in content.items():
        if key == "args":
            continue
        elif key == "resources":
            txt = ""
            for k, v in val.items():
                txt += f"{k} = {v}, "
            if txt:
                txt = txt[:-2]
        else:
            txt = fmt_date(val)
        print_tab(key, txt)
    args = content["args"]
    echo("\nArguments:")
    for a in args:
        print_tab("", a)
    secho("\nNode status", bold=True)
    node_id = content["node_id"]
    url = ctx.obj.session.knode_url + f"/nodes/{node_id}"
    try:
        resp = ctx.obj.session.get(url)
    except ServerError:
        abort(f"Node {node_id} not found. This job is probably invalid.")
    node = resp.json()
    for k in [
        "node_id",
        "status",
        "modified_date",
        "registered",
        "instance_type",
        "availability_zone",
        "ami_id",
    ]:
        print_tab(k, node.get(k))
    resources = node.get("resource_allocations")
    if resources:
        print_tab("CPU Allocation", f"{resources['cpu']['current']}/{resources['cpu']['max']}")
        print_tab("RAM Allocation", f"{resources['ram']['current']}/{resources['ram']['max']}")
        print_tab("Utilization", f"{resources['utilization']}%")
    echo("")


@app.command("shutdown")
def shutdown_job(
    ctx: Context,
    job_id: str = Argument(..., help="Job ID to shut down"),
    is_force: bool = Option(False, "-y", is_flag=True, help="Force a shutdown without a prompt"),
):
    """Shut down the selected job by ID"""
    url = ctx.obj.session.knode_url + f"/jobs/{job_id}"
    try:
        resp = ctx.obj.session.get(url)
    except ServerError as ex:
        abort(ex)

    content = resp.json()
    job_id = content["job_id"]
    tenant = content["tenant"]
    if not is_force:
        confirm(
            f"Are you sure you want to shut down job '{job_id}' for the '{tenant}' tenant?",
            abort=True,
        )

    resp = ctx.obj.session.patch(url, json={"status": "shutdown"})

    if ctx.obj.output == "json":
        output = {"job": job_id, "tenant": tenant, "success": True, "command": "shutdown"}
        echo(json.dumps(output))
    else:
        secho(f"job '{job_id}' for tenant '{tenant}' is being shut down")


@app.command("delete")
def delete_job(
    ctx: Context,
    job_id: str = Argument(..., help="Job ID to shut down"),
    is_force: bool = Option(False, "-y", is_flag=True, help="Force a delete without a prompt"),
):
    """Delete the selected job by ID (dangerous!)"""
    url = ctx.obj.session.knode_url + f"/jobs/{job_id}"
    try:
        resp = ctx.obj.session.get(url)
    except ServerError as ex:
        abort(ex)

    content = resp.json()
    job_id = content["job_id"]
    tenant = content["tenant"]
    if not is_force:
        confirm(
            f"Are you sure you want to shut down job '{job_id}' for the '{tenant}' tenant?",
            abort=True,
        )

    resp = ctx.obj.session.delete(url)

    if ctx.obj.output == "json":
        output = {"job": job_id, "tenant": tenant, "success": True, "command": "shutdown"}
        echo(json.dumps(output))
    else:
        secho(f"job '{job_id}' for tenant '{tenant}' has been shut down")


@app.command("shutdown-all")
def shutdown_all(
    ctx: Context,
    is_force: bool = Option(False, "-y", is_flag=True, help="Force a shutdown without a prompt"),
    is_wait: bool = Option(False, "-w", "--wait", is_flag=True, help="Wait until jobs have been shut down"),
):
    """Shut down all jobs in the current tenant"""
    tenant = ctx.obj.tenant
    if not is_force:
        if ctx.obj.is_all:
            confirm(
                f"Are you sure you want to shut down ALL jobs for ALL tenants on the server?",
                abort=True,
            )
        else:
            confirm(
                f"Are you sure you want to shut down all jobs for the '{tenant}' tenant?",
                abort=True,
            )

    if ctx.obj.is_all:
        tenant = None
    url = ctx.obj.session.knode_url + f"/jobs"
    params = {"tenant": tenant, "start": 0, "end": 100, "status": "pending,processing,running"}
    resp = ctx.obj.session.get(
        url,
        params=params,
    )
    jobs = resp.json()
    cnt = len(jobs)
    for job in jobs:
        job_url = url + "/" + str(job["job_id"])
        _ = ctx.obj.session.patch(job_url, json={"status": "shutdown"})

    if is_wait:
        start_time = time.time()
        while time.time() < start_time + 30.0:
            resp = ctx.obj.session.get(
                url,
                params=params,
            )
            n = len(resp.json())
            if n <= 0:
                break
            out(f"Waiting for {n} jobs to stop")
            time.sleep(1.0)
        if n == 0:
            success(f"{cnt} jobs have been shut down for tenant '{tenant}'", bold=True)
        else:
            out(f"Timeout waiting for {n} jobs to stop", fg="red")
            out(
                f"It is possible that there are dead ec2 instances in which case you will need to delete jobs.\nYou can investigate this by running 'kamo nodes list' and then delete jobs with 'kamo jobs delete-all'."
            )

            sys.exit(1)
    else:
        if ctx.obj.is_all:
            success(
                f"{cnt} jobs are being shut down. All jobs on server have been sent the shutdown signal.",
                bold=True,
            )
        else:
            success(f"{cnt} jobs are being shut down for tenant '{tenant}'", bold=True)


@app.command("delete-all")
def delete_all(
    ctx: Context, is_force: bool = Option(False, "-y", is_flag=True, help="Force a delete without a prompt")
):
    """Delete all jobs in the current tenant (dangerous!)"""
    tenant = ctx.obj.tenant
    if not is_force:
        if ctx.obj.is_all:
            confirm(
                f"Are you sure you want to permanently delete ALL jobs for ALL tenants on the server?",
                abort=True,
            )
        else:
            confirm(
                f"Are you sure you want to permanently delete all jobs for the '{tenant}' tenant?",
                abort=True,
            )

    if ctx.obj.is_all:
        tenant = None
    url = ctx.obj.session.knode_url + f"/jobs"
    resp = ctx.obj.session.get(url, params={"tenant": tenant, "start": 0, "end": 100, "status": ""})
    for job in resp.json():
        job_url = url + "/" + str(job["job_id"])
        _ = ctx.obj.session.delete(job_url)

    cnt = len(resp.json())
    if ctx.obj.is_all:
        success(
            f"{cnt} jobs have been deleted. All jobs on server have been removed.",
            bold=True,
        )
    else:
        success(f"{cnt} jobs have been deleted for tenant '{tenant}'", bold=True)


@app.command("cleanup")
def cleanup(ctx: Context):
    """Clean up orphaned jobs (with no node running) for the current tenant."""
    tenant = ctx.obj.tenant
    if ctx.obj.is_all:
        tenant = None
    jobs_url = ctx.obj.session.knode_url + f"/jobs"
    resp = ctx.obj.session.get(
        jobs_url, params={"tenant": tenant, "start": 0, "end": 100, "status": "running,pending,processing"}
    )
    n = 0
    for job in resp.json():
        node_id = job["node_id"]
        url = ctx.obj.session.knode_url + f"/nodes/{node_id}"
        try:
            ctx.obj.session.get(url)
            continue
        except ServerError as e:
            if e.response["status_code"] == 404:
                out(f"Deleting orphaned job {job['job_id']} on node {job['node_id']} in tenant {job['tenant']}")
                job_url = jobs_url + "/" + str(job["job_id"])
                _ = ctx.obj.session.delete(job_url)
                n += 1
    if n:
        success(f"Done cleaning up {n} jobs", bold=True)
    else:
        success(f"No orphaned jobs to clean up", bold=True)

@app.command("duplicate")
@check_tenant
def duplicate_job(ctx: Context, job_id: str):
    """
    Create an new job which is identical to an existing job.
    Use a comma-separated list of job id's to duplicate multiple jobs.
    """
    for j in job_id.split(","):
        j = j.strip()
        tenant = ctx.obj.tenant
        url = ctx.obj.session.knode_url + f"/jobs/{j}"
        resp = ctx.obj.session.get(url)
        resp.raise_for_status()
        job =  resp.json()
        version = job["version"]
        s3_path = job["s3_path"]
        cpu = job["resources"].get("cpu", 0)
        mem = job["resources"].get("ram", "0 GB")
        map_name = job["map_name"]
        executable = job["executable"]
        args = job["args"]
        data = {
            "tenant": tenant,
            "tenant_only": True,
            "version": version or "none",
            "map_name": map_name,
            "resources": {"cpu": cpu, "ram": mem},
            "executable": executable,
            "s3_path": s3_path,
            "args": args,
        }
        url = ctx.obj.session.knode_url + f"/jobs"
        try:
            resp = ctx.obj.session.post(url, json=data)
        except ServerError as ex:
            abort(ex)
        content = resp.json()
        if ctx.obj.output == "json":
            print(json.dumps(content, indent=2))
        else:
            new_job_id = content["job_id"]
            secho(f"Job {new_job_id} created from job {j}", bold=True)

@app.command("create")
@check_tenant
def create_job(
    ctx: Context,
    s3_path: str = Option(None, "--s3", help="Deploy a specific build from S3"),
    version: str = Option(None, "-v", "--version", help="Version to deploy (or latest)"),
    cpu: int = Option(0, "-c", "--cpu", help="Amount of CPU's to reserve"),
    mem: str = Option("0 GB", "-m", "--mem", help="Amount of memory to reserve"),
    node_id: str = Option(None, "-n", "--node", help="Pick a specific node to run on"),
    volumes: str = Option(None, "--volumes", help="Level Volumes to load."),
    process_per_volume: bool = Option(
        False,
        "--ppv",
        is_flag=True,
        help="Deploy one process per Kamo Volume.",
    ),
    instance_id: str = Option(None, "-i", "--instance-id", help="Level instance ID."),
    executable: str = Option(None, "-e", "--executable", help="Executable name and path (if not standard)"),
    map_name: str = Option(
        None,
        "--map",
        help="Run a custom map or game mode, injected into the head of the command line",
    ),
    custom_args: str = Option("?listen,-server,-NullRHI", "-a", "-args", help="Override default arguments"),
    is_force: bool = Option(
        False,
        "-y",
        is_flag=True,
        help="Create the requested jobs without a prompt",
    )
):
    """Create a new job. Deploy the most recent server build by default"""
    tenant = ctx.obj.tenant
    builds_path = ctx.obj.session.profile.builds_path

    if version and not builds_path:
        abort("You must set a build path with 'kamo builds path' to deploy a versioned build")

    if not version and not s3_path:
        abort("You must specify either a version (or latest) or s3_path")

    if process_per_volume:
        if not map_name and not volumes:
            abort(f"Map name or volumes must be specified when using --ppv option.")

        if map_name and not volumes:
            # PROVISIONAL: Enumerate regions, find the map, parse the name to get the volumes.
            map_name = map_name.lower()

            volumes_per_map = {}
            for region_name in find_regions(ctx):
                region_map_name, volume_name, region_instance_id = parse_region_name(region_name)
                print(f"Region: {region_map_name} {volume_name} {region_instance_id}")
                if instance_id != region_instance_id:  # We need exact match for the region
                    continue
                volumes_per_map.setdefault(region_map_name, []).append(volume_name)

            if map_name not in volumes_per_map:
                abort(
                    f"Map '{map_name}' not found on DB, only these exist: {list(volumes_per_map.keys())}.\nTry deploy without the --ppv switch to populate the DB."
                )

            volumes = " ".join([volume or "main" for volume in volumes_per_map[map_name]])

    args = [c.strip() for c in custom_args.split(",")]
    if not s3_path:
        versions = {}
        versions = get_builds_from_s3_url(builds_path)
        if not versions:
            abort(f"No builds found")
        if version != "latest":
            if version not in versions:
                abort(
                    f"Version '{version}' not found for tenant '{tenant}'.\nAvailable versions: {', '.join(versions.keys())}"
                )
        else:
            version = list(versions.keys())[0]
        s3_path = versions[version]["s3_path"]

    client = boto3.client("s3")
    parts = urlparse(s3_path)
    bucket_name = parts.netloc
    prefix = parts.path[1:]

    try:
        f = BytesIO()
        client.download_fileobj(bucket_name, prefix + "buildinfo.json", f)
        f.seek(0)
        build_info = json.load(f)
        if not version:
            version = build_info.get("version", "N/A")
        if not executable:
            executable = build_info.get("executable")
    except Exception as e:
        secho(f"Could not load buildinfo.json from {s3_path}. Was the path correct? Error: {e}", fg="red")

    if not executable:
        abort("You must specify an executable to run. e.fg. 'LinuxServer/TestProject/Binaries/Linux/TestProject'")

    all_nodes = find_nodes(ctx)
    if node_id:
        node_ids = all_nodes.keys()
        if node_id not in node_ids:
            abort(f"Node {node_id} not found")

    if instance_id:
        args.append(f"-kamoinstanceid={instance_id}")

    if volumes and not process_per_volume:
        # Add all the volumes on a single node
        args.append(f"-kamovolumes={volumes}")

    if process_per_volume:
        launches = volumes.split(" ")
    else:
        launches = [None]

    if not is_force:
        confirm(
            f"Do you want to create {len(launches)} jobs with version '{version}' from '{s3_path}' on the '{tenant}' tenant with executable '{executable}'?",
            abort=True,
        )

    responses = []
    for volume in launches:
        data = {
            "node_id": node_id,
            "tenant": tenant,
            "tenant_only": True,
            "version": version or "none",
            "map_name": map_name,
            "resources": {"cpu": cpu, "ram": mem},
            "executable": executable,
            "s3_path": s3_path,
            "args": copy.copy(args),
        }

        if process_per_volume:
            data["args"].append(f"-kamovolumes={volume}")

        log.info(
            f"Creating job with version {version} on 'region.{map_name}^{volume}#{instance_id}' for tenant {tenant}"
        )
        url = ctx.obj.session.knode_url + f"/jobs"
        try:
            resp = ctx.obj.session.post(url, json=data)
        except ServerError as ex:
            abort(ex)
        content = resp.json()
        responses.append(content)

    if ctx.obj.output == "json":
        echo(dumps(responses))
    else:
        for response in responses:
            job_id = response["job_id"]
            echo(f"job '{job_id}' created for tenant '{tenant}' with version {version}")


@app.command("maps")
def list_maps(
    ctx: Context,
    map_name_filter: str = Option(
        None,
        "--map",
        help="Only show this map",
    ),
    instance_filter: str = Option(
        None,
        "--instance",
        help="Only show this instance",
    ),
):
    """List maps available for jobs to deploy"""

    # PROVISIONAL: Enumerate regions, find the map, parse the name to get the volumes.
    if map_name_filter:
        map_name_filter = map_name_filter.lower()

    instances = {}
    for region_name in find_regions(ctx):
        map_name, volume_name, instance_id = parse_region_name(region_name)
        """
        print(f"Region: {region_map_name} {volume_name} {region_instance_id}")

        Region: map_main_p None None
        Region: map_worldglacier01_p volume_town01 None
        Region: map_worldglacier01_p None None
        """
        volume_name = volume_name or "main"
        instance_id = instance_id or "main"

        if map_name_filter and map_name != map_name_filter:
            continue
        if instance_filter and instance_filter != instance_id:
            continue

        instances.setdefault(instance_id, {}).setdefault(map_name, []).append(volume_name)

    if ctx.obj.output == "json":
        print(json.dumps(instances, indent=4))
    else:
        from textwrap import indent

        for instance_id, maps in instances.items():
            if len(instances) > 0:
                print(f"Instance: {instance_id}")
                fill = "    "
            else:
                fill = ""

            for map_name, volumes in maps.items():
                print(indent(f"{map_name}: {volumes}", fill))
