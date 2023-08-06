import click
import logging
import kamocli
import requests
import dateutil.parser
import json
import datetime
import time
from time import sleep
from kamocli.utils import dumps, abort, print_tab, fmt_date, check_tenant, success, out
from kamosdk.exceptions import ServerError
from tabulate import tabulate

log = logging.getLogger(__name__)

from typer import Typer, Context, Argument, Option, echo, secho, confirm

app = Typer()


@app.callback(
    help="Manage EC2 server instances",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def cli(ctx: Context):
    pass


DEFAULT_INSTANCE_TYPE = "m5a.large"

def is_dead(node):
    last_modified = dateutil.parser.parse(node["modified_date"])
    if node["status"] != "running" or last_modified < datetime.datetime.utcnow() - datetime.timedelta(minutes=2):
        return True
    return False


@app.command("ensure")
@check_tenant
def ensure(
    ctx: Context,
    num: int = Argument(..., help="Number of instances"),
    instance_type: str = Option(DEFAULT_INSTANCE_TYPE, "--type", "-t", help="Type of EC2 instance to launch"),
    is_wait: bool = Option(False, "-w", "--wait", is_flag=True, help="Wait until instance is ready"),
):
    """
    Make sure that the specified number of instances are
    running on the tenant and terminate excessive instances if needed.
    Also cleans up any zombie entries in knode to make things nice and tidy.
    """
    MAX_NUM = 6
    if num > MAX_NUM:
        abort(f"You can ensure at most {MAX_NUM} instances")
    tenant = ctx.obj.session.profile.tenant
    nodes = find_nodes(ctx, tenant)
    if nodes:
        for node in nodes:
            if is_dead(node):
                out("Removing broken instance %s" % node["node_id"])
                url = ctx.obj.session.knode_url + f"/nodes/{node['node_id']}"
                try:
                    resp = ctx.obj.session.delete(url)
                    resp.raise_for_status()
                except Exception as e:
                    abort(
                        f"Could not remove broken instance {node['node_id']}. Please delete it manually before continuing."
                    )
        nodes = find_nodes(ctx, tenant)

    num_nodes_to_launch = num - len(nodes)
    if num_nodes_to_launch <= 0:
        txt = f"Tenant has {len(nodes)} running nodes and no nodes need to be launched\n"
        for node in nodes:
            txt += node["node_id"] + "\n"
        success(txt)

    url = ctx.obj.session.knode_url + "/nodes"
    data = {"instance_type": instance_type}
    tenant = ctx.obj.session.profile.tenant
    data["tenant"] = tenant
    out(f"Launching {num_nodes_to_launch} nodes for tenant {tenant}")
    new_nodes = []
    for i in range(num_nodes_to_launch):
        try:
            resp = ctx.obj.session.post(url, json=data)
            new_nodes.append(resp.json()["node_id"])
        except ServerError as ex:
            abort(ex.message)

    if is_wait:
        node_infos = wait_for_nodes(ctx, new_nodes)
        txt = "All nodes ready!\n"
        for node_id, node_info in node_infos.items():
            status = node_info["status"]
            txt += f"Node {node_id} is in state '{status}'\n"
        success(txt)
    else:
        success(f"{num_nodes_to_launch} nodes are being started")


@app.command("launch")
def launch(
    ctx: Context,
    instance_type: str = Option(DEFAULT_INSTANCE_TYPE, "--type", "-t", help="Type of EC2 instance to launch"),
    is_all: bool = Option(
        False,
        "-a",
        "--all",
        is_flag=True,
        help="Node should not have node affinity but be available to all tenants",
    ),
    is_wait: bool = Option(False, "-w", "--wait", is_flag=True, help="Wait until instance is ready"),
):
    """
    Launch a new EC2 instance
    """
    url = ctx.obj.session.knode_url + "/nodes"
    data = {"instance_type": instance_type}
    if not is_all:
        data["tenant"] = ctx.obj.session.profile.tenant
    try:
        resp = ctx.obj.session.post(url, json=data)
    except ServerError as ex:
        abort(ex.message)
    node_id = resp.json()["node_id"]
    if not ctx.obj.output == "json":
        secho(f"EC2 instance {node_id} is being launched...")
    if is_wait:
        node_info = wait_for_nodes(ctx, [node_id])[0]
        status = node_info["status"]
        success(f"Node {node_id} is in state '{status}'")


def wait_for_nodes(ctx, node_ids):
    start_time = time.time()
    url = ctx.obj.session.knode_url + "/nodes"
    ready_nodes = {}
    while len(node_ids) > len(ready_nodes):
        sleep(5.0)
        for node_id in node_ids:
            node_info = ctx.obj.session.get(url + f"/{node_id}").json()
            status = node_info["status"]
            if status != "launching":
                ready_nodes[node_id] = node_info
        diff = time.time() - start_time
        nodes = [n for n in node_ids if n not in ready_nodes]
        if nodes:
            txt = ", ".join(nodes)
            out(f"[{diff:.0f}s] Waiting for instances to become ready: {txt}")
    return ready_nodes


def find_nodes(ctx, tenant=None):
    resp = ctx.obj.session.get(ctx.obj.session.knode_url + "/nodes")
    resp.raise_for_status()
    nodes = resp.json()
    if tenant:
        nodes = [n for n in nodes if n.get("tenant") == tenant]
    return nodes


@app.command("list")
@check_tenant
def list_nodes(
    ctx: Context,
    is_all: bool = Option(
        False,
        "-a",
        "--all",
        is_flag=True,
        help="View all nodes on the server, not just for my tenant",
    ),
):
    """
    List Nodes
    """
    tenant = ctx.obj.session.profile.tenant if not is_all else None
    nodes = find_nodes(ctx, tenant)

    if ctx.obj.output == "json":
        echo(dumps(nodes))
        return

    if not nodes:
        if is_all:
            abort("No nodes running on server")
        else:
            abort(
                f"No nodes running available to tenant '{tenant}'. Rerun this command with the --all flag to see all nodes."
            )

    node_list = []
    columns = ["node_id", "status", "create_date", "modified_date", "instance_type", "tenant", "ip_address"]
    for node in nodes:
        node_row = []
        status = node["status"]
        if status == "running" and is_dead(node):
            status += " (offline)"

        for k in columns:
            v = node.get(k)
            v = fmt_date(v)
            if k == "status":
                v = status
                if v != "running":
                    v = click.style(v, fg="red")
            node_row.append(v)
        resources = node.get("resource_allocations")
        if resources:
            node_row.append(f"{resources['cpu']['current']}/{resources['cpu']['max']}")
            node_row.append(f"{resources['ram']['current']}/{resources['ram']['max']}")
            node_row.append(f"{resources['utilization']}%")
        node_list.append(node_row)
    columns.append("CPU")
    columns.append("RAM")
    columns.append("Utilization")
    echo(tabulate(node_list, headers=columns))


@app.command("terminate-all")
def terminate_all(
    ctx: Context,
    is_all: bool = Option(False, "-a", "--all", is_flag=True, help="Teminate all nodes for all tenants"),
    is_force: bool = Option(False, "-y", is_flag=True, help="Force a delete without a prompt"),
):
    """
    Terminate all nodes for the tenant
    """
    tenant = ctx.obj.session.profile.tenant if not is_all else None
    nodes = find_nodes(ctx, tenant)
    if not nodes:
        abort("No EC2 nodes found")
    if not is_force:
        if is_all:
            confirm(
                f"Are you sure you want to terminate {len(nodes)} EC2 instances for ALL tenants on the server?",
                abort=True,
            )
        else:
            confirm(
                f"Are you sure you want to terminate {len(nodes)} EC2 instances for the '{tenant}' tenant?",
                abort=True,
            )

    for node in nodes:
        url = ctx.obj.session.knode_url + f"/nodes/{node['node_id']}"

        resp = ctx.obj.session.delete(url)
        resp.raise_for_status()
    success(f"{len(nodes)} EC2 instances are being terminated")


@app.command("view")
def view(ctx: Context, node_id: str = Argument(..., help="EC2 Instance ID to view")):
    """
    View a specific EC2 instance
    """
    url = ctx.obj.session.knode_url + f"/nodes/{node_id}"

    try:
        resp = ctx.obj.session.get(url)
    except ServerError as ex:
        abort(ex)
    node = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(node))
        return

    for k in [
        "node_id",
        "status",
        "last_modified",
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


@app.command()
def terminate(
    ctx: Context,
    node_id: str = Argument(..., help="EC2 Instance ID to terminate"),
    is_force: bool = Option(False, "-y", is_flag=True, help="Force a delete without a prompt"),
):
    """
    Terminate an EC2 Instance
    """
    url = ctx.obj.session.knode_url + f"/nodes/{node_id}"

    try:
        _ = ctx.obj.session.get(url)
    except ServerError as ex:
        abort(ex)

    if not is_force:
        confirm(
            f"Are you sure you want to terminate node {node_id}?",
            abort=True,
        )

    resp = ctx.obj.session.delete(url)
    resp.raise_for_status()
    echo(f"Node {node_id} has been terminated")
