import logging
import requests
import dateutil
import json
from tabulate import tabulate
import tempfile
import collections

from kamosdk.exceptions import ServerError
from kamosdk.utils import generate_kamo_id
import kamocli
from kamocli.utils import (
    dumps,
    abort,
    print_tab,
    print_table,
    check_tenant,
    get_tenant_url,
    success,
    find_regions,
    find_builds,
    fmt_date,
    out,
)

log = logging.getLogger(__name__)

from typer import Typer, Context, Argument, Option, echo, secho, confirm, edit

app = Typer()


@app.callback(
    help="Kamo database management",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def cli(ctx: Context):
    ctx.obj.tenant = ctx.obj.session.profile.tenant


@app.command("stats")
@check_tenant
def stats(ctx: Context):
    """
    View Kamo DB statistics
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.get(url + "/db/stats")
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return

    secho(f"\nStatistics for tenant {tenant}:\n", bold=True)
    lst = [list(content["counts"].values())]
    headers = list(content["counts"].keys())
    echo(tabulate(lst, headers=headers))

    if content["most_populated_regions"]:
        secho("\nMost populated regions:\n", bold=True)
        lst = []
        for region in content["most_populated_regions"]:
            lst.append([region["id"], region["objects"]])
        echo(tabulate(lst, headers=["region", "objects"]))

    if content["most_common_classes"]:
        secho("\nMost common classes:\n", bold=True)
        lst = []
        for instance in content["most_common_classes"]:
            lst.append([instance["kamo_class"], instance["instances"]])
        echo(tabulate(lst, headers=["Class", "Instances"]))
    echo("")


@app.command("clear")
def clear(
    ctx: Context,
    y: bool = Option(False, "-y", is_flag=True, help="Override 'Are you sure' prompt"),
):
    """
    Delete all kamo objects and regions from the database
    """
    session = ctx.obj.session
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    if not y:
        confirm(
            f"Are you sure you want to delete the Kamo DB for the '{ctx.obj.tenant}' tenant?",
            abort=True,
        )
    session.delete(url + "/db")
    success(f"The database for '{ctx.obj.tenant}' has been cleared", fg="yellow", bold=True)


objects_app = Typer()
app.add_typer(objects_app, name="objects", help="Manage kamo objects")


@objects_app.command("list")
def objects(
    ctx: Context,
    class_name: str = Option("", "-c", "--class", help="Filter by object class"),
    kamo_id: str = Option("", "-k", "--kamo_id", help="filter on kamo_id"),
    region_id: str = Option("", "-r", "--region_id", help="filter on region_id"),
    num: int = Option(100, "-n", help="Maximum number of results"),
):
    """
    View list of all kamo objects in all regions
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    tenant_url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    url = tenant_url + f"/db/objects?kamo_id={kamo_id}&class_name={class_name}&region_id={region_id}&end={num}"
    resp = session.get(url)
    content = resp.json()

    if ctx.obj.output == "json":
        echo(dumps(content))
        return

    lst = []
    for obj in content:
        lst.append([obj["id"], obj["region_id"]])

    if not lst:
        abort(f"No objects found for tenant {tenant}")

    headers = ["ID", "Region"]
    headers.extend(["Handler", "IP address"])
    secho(f"\nFound {len(lst)} objects for tenant {tenant}", bold=True)
    if len(lst) >= num:
        secho(f"Note that only the top {num} items are returned")
    echo(tabulate(lst, headers=headers))
    echo("")


@objects_app.command("report")
def report(
    ctx: Context,
):
    """
    Kamo item report for the current tenant
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    tenant_url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    url = tenant_url + f"/db/objects?end=9999999"
    resp = session.get(url)
    content = resp.json()

    if ctx.obj.output == "json":
        echo(dumps(content))
        return

    items_by_class = collections.defaultdict(int)
    items_by_region = collections.defaultdict(int)
    for obj in content:
        class_name = obj["id"].split(".")[0]
        items_by_class[class_name] += 1
        items_by_region[obj["region_id"]] += 1

    secho("Items by region", bold=True)

    headers = ["Region", "Count"]
    lst = []
    for k, v in items_by_region.items():
        lst.append((k, v))
    echo(tabulate(lst, headers=headers))
    echo("")

    secho("Items by object class", bold=True)

    headers = ["Class", "Count"]
    lst = []
    for k, v in items_by_class.items():
        lst.append((k, v))
    echo(tabulate(sorted(lst), headers=headers))
    echo("")


@objects_app.command("cleanup")
def delete(
    ctx: Context,
    class_name: str,
    region_id: str = Option("", "-r", "--region_id", help="filter on region_id"),
    y: bool = Option(False, is_flag=True, help="Override 'Are you sure' prompt"),
):
    """
    Delete multiple kamo objects by class.

    TODO: Temporarily just call delete for each object. Needs to be refactored
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    tenant_url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    url = tenant_url + f"/db/objects?class_name={class_name}&region_id={region_id}&end=99999"
    resp = session.get(url)
    content = resp.json()
    if not y:
        confirm(
            f"Are you sure you want to delete {len(content)} kamo objects in the '{tenant}' tenant?",
            abort=True,
        )

    for item in content:
        kamo_id = item["id"]
        url = tenant_url + f"/db/objects/{kamo_id}"
        out(f"Deleting item {kamo_id}")
        try:
            resp = session.delete(url)
        except ServerError as ex:
            abort(ex)
    success(f"{len(content)} items have been deleted from the '{tenant}' tenant")


object_app = Typer()
app.add_typer(object_app, name="object", help="Manage a single kamo object")


@object_app.callback(
    help="Object management",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def cli(ctx: Context, kamo_id: str = Argument(..., help="Kamo ID of the object")):
    from urllib.parse import quote

    ctx.obj.kamo_id = quote(kamo_id)


@object_app.command("delete")
def delete(ctx: Context):
    """
    Delete the kamo object
    """
    kamo_id = ctx.obj.kamo_id
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    tenant_url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    url = tenant_url + f"/db/objects/{kamo_id}"
    try:
        resp = session.delete(url)
    except ServerError as ex:
        abort(ex)


regions_app = Typer()
app.add_typer(regions_app, name="regions", help="Manage kamo regions")


@object_app.command("view")
def view_object(ctx: Context):
    """
    View a kamo object
    """
    kamo_id = ctx.obj.kamo_id
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    tenant_url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    url = tenant_url + f"/db/objects/{kamo_id}"
    try:
        resp = session.get(url)
    except ServerError as ex:
        abort(ex)
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return

    content["state"] = "(%s items)" % len(content.get("state", {}))
    print_table(content)

    region_id = content["region_id"]
    if region_id and region_id != kamo_id:
        out("\n")
        region_report(ctx, region_id)


@object_app.command("state")
def state_object(ctx: Context):
    """
    View a kamo object's state
    """
    kamo_id = ctx.obj.kamo_id
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    tenant_url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    url = tenant_url + f"/db/objects/{kamo_id}"
    try:
        resp = session.get(url)
    except ServerError as ex:
        abort(ex)
    content = resp.json()
    state = content.get("state", {})
    if ctx.obj.output == "json":
        echo(dumps(state))
        return

    secho(f"\nViewing state for object {kamo_id}\n", bold=True)
    for k, v in state.items():
        print_tab(k, v)


@object_app.command("edit")
def edit_object(ctx: Context, key: str = Option(None, "-k", "--key", help="Edit a specific key")):
    """
    Edit a kamo object state directly
    """
    kamo_id = ctx.obj.kamo_id
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    tenant_url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    url = tenant_url + f"/db/objects/{kamo_id}"
    try:
        resp = session.get(url)
    except ServerError as ex:
        abort(ex)
    state = resp.json()["state"]
    if key:
        js = state[key]
    else:
        js = state
    with tempfile.NamedTemporaryFile() as fp:
        txt = json.dumps(js, indent=4, default=str)
        while 1:
            out_txt = edit(txt)
            if not out_txt:
                abort("No changes were made")
            try:
                js = json.loads(out_txt)
                break
            except Exception as e:
                out(f"Json is invalid: {e}", fg="red")
                confirm("Would you like to open the editor again?", abort=True)
                txt = out_txt

        if key:
            state[key] = js
        else:
            state = js
        resp = session.put(url, json=state)
        if "message" in resp.json():
            success(resp.json()["message"])
        else:
            abort(str(resp.json()))


def region_report(ctx, region_id):
    out(f"Region {region_id}:")
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    tenant_url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    url = tenant_url + f"/db/regions/{region_id}"
    resp = session.get(url)
    content = resp.json()
    content["state"] = "(%s items)" % len(content.get("state", {}))
    print_table(content)
    handler_url = content["handler_url"]
    if handler_url:
        try:
            resp = session.get(handler_url)
            content = resp.json()
            server_id = content["id"]
            secho(f"\nHandler {server_id}:")
            content["state"] = "(%s items)" % len(content.get("state", {}))
            print_table(content)
        except ServerError:
            out(f"No Unreal server is currently handling region {region_id}")


regions_app = Typer()
app.add_typer(regions_app, name="regions", help="Manage kamo regions")


@regions_app.command("list")
@check_tenant
def list_regions(ctx: Context):
    """
    List Kamo regions
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.get(url + "/db/regions?start=0&end=100")
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return
    secho(f"Tenant {ctx.obj.tenant} is handling the following regions:")
    lst = []
    for region in resp.json()["regions"]:
        lst.append([region["id"], region["handler_id"]])

    if not lst:
        abort(f"No regions found for tenant {tenant}")

    echo(f"Regions for tenant {tenant}:")
    echo(tabulate(lst, headers=["ID", "Handler"]))


@regions_app.command("create")
@check_tenant
def create_region(
    ctx: Context,
    region: str = Argument(..., help="Kamo ID of region to create"),
    state: str = Option('{"handler": ""}', "-s", "--state", show_default=True, help="Region initial state"),
):
    """
    Create a new kamo region. Use a comma-separated list to create multiple identical regions
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, tenant)
    state = json.loads(state)
    regions = [r.strip() for r in region.split(",")]
    result = ""
    for region in regions:
        data = {"id": region, "state": state}
        try:
            resp = session.post(url + f"/db/regions/", json=data)
        except ServerError as ex:
            abort(ex)
        content = resp.json()
        result += f"\nRegion '{region}' has been created in tenant '{tenant}'"
    success(result)


@regions_app.command("delete-all")
@check_tenant
def delete_all_regions(
    ctx: Context,
    y: bool = Option(False, is_flag=True, help="Override 'Are you sure' prompt"),
):
    """
    Delete all kamo regions
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, tenant)
    regions = find_regions(ctx)
    if not regions:
        abort(f"Tenant '{tenant}' has no regions")
    if not y:
        confirm(
            f"Are you sure you want to delete {len(regions)} regions in the '{tenant}' tenant?",
            abort=True,
        )

    for region in regions:
        _ = session.delete(url + f"/db/regions/{region}")
    success(f"{len(regions)} have been deleted in tenant '{tenant}'")


region_app = Typer()
app.add_typer(region_app, name="region", help="Manage a single kamo region")


@region_app.callback(
    help="Region management",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def cli(ctx: Context, region: str = Argument(..., help="Kamo ID of region to view")):
    ctx.obj.region = region


@region_app.command("view")
def view_region(ctx: Context):
    """
    View a single kamo region
    """
    region = ctx.obj.region
    session = ctx.obj.session
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.get(url + f"/db/regions/{region}")
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return
    print_table(content)


@region_app.command("delete")
def delete_region(
    ctx: Context,
    y: bool = Option(False, is_flag=True, help="Override 'Are you sure' prompt"),
):
    """
    Delete the selected kamo region
    """
    region = ctx.obj.region
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, tenant)
    try:
        _ = session.get(url + f"/db/regions/{region}")
    except ServerError as ex:
        abort(ex)
    if not y:
        confirm(
            f"Are you sure you want to delete region {region} from the '{ctx.obj.tenant}' tenant?",
            abort=True,
        )

    resp = session.delete(url + f"/db/regions/{region}")
    success(f"Region '{region}' has been deleted in tenant '{tenant}'")


@region_app.command("create-object")
def region_create_object(
    ctx: Context,
    class_name: str,
    kamo_id: str = Option(None, "-k", "--kamo-id", help="Unique kamoID (optional)"),
    state: str = Option("{}", "-s", "--state", help="Initial kamo state for the object"),
):
    """
    Create an object in the region
    """
    region = ctx.obj.region
    session = ctx.obj.session
    kamo_id = kamo_id or generate_kamo_id(class_name)
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    data = {"id": kamo_id, "region_id": region, "state": json.loads(state)}
    try:
        resp = session.post(f"{url}/db/objects", json=data)
    except ServerError as ex:
        abort(ex)
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return
    success(f"Kamo object {kamo_id} has been created in region {region}")


@region_app.command("delete-object")
def region_delete_object(ctx: Context, kamo_id: str):
    """
    delete a specific object in the region
    """
    region = ctx.obj.region
    session = ctx.obj.session
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.delete(f"{url}/db/objects/{kamo_id}?region_id={region}")
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return
    success(f"Kamo object {kamo_id} has been deleted in region {region}")


@region_app.command("delete-object-class")
def region_delete_objects_class(ctx: Context, class_name: str):
    """
    delete all object by class in the region
    """
    region = ctx.obj.region
    session = ctx.obj.session
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.delete(f"{url}/db/objects/?class_name={class_name}&region_id={region}")
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return
    msg = content.get("message")
    success(f"Kamo objects with class {class_name} have been deleted in region {region}. Server response: {msg}")


@region_app.command("objects")
def region_objects(ctx: Context, class_name: str = Option("", "-c", "--class", help="Filter by object class")):
    """
    View a list of objects in the region
    """
    region = ctx.obj.region
    session = ctx.obj.session
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.get(f"{url}/db/objects?start=0&end=1000&region_id={region}&class_name={class_name}")
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return
    objects = content
    lst = []
    for obj in objects:
        lst.append([obj["id"], obj["region_id"]])
    echo(tabulate(lst, headers=["kamo_id", "region_id"]))
    echo("")


@app.command("handlers")
def handlers(ctx: Context):
    """
    View list of all kamo handlers
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.get(url + "/db/handlers?start=0&end=100&full_state=true")
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return
    secho(f"Tenant {ctx.obj.tenant} has the following handlers:")
    lst = []
    for handler in resp.json()["handlers"]:
        state = handler["state"]
        handler_row = [handler["id"], state["ip_address"] + ":" + str(state["port"])]
        handler_row.append(dateutil.parser.parse(state["start_time"]).strftime("%Y-%m-%d %H:%M"))
        handler_row.append(dateutil.parser.parse(state["last_refresh"]).strftime("%Y-%m-%d %H:%M"))
        lst.append(handler_row)

    if not lst:
        abort(f"No handlers found for tenant {tenant}")

    echo(f"Handlers for tenant {tenant}:")

    echo(tabulate(lst, headers=["ID", "IP Address", "Created", "Updated"]))


@regions_app.command("clear-handlers")
def clear_handlers(
    ctx: Context,
    y: bool = Option(False, "-y", is_flag=True, help="Override 'Are you sure' prompt"),
):
    """
    Clear all handlers from all regions (debug only!)
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    regions = find_regions(ctx)
    if not y:
        confirm(
            f"Are you sure you want to clear handlers from {len(regions)} regions in the '{ctx.obj.tenant}' tenant?",
            abort=True,
        )
    for region in regions:
        resp = session.get(url + f"/db/regions/{region}")
        content = resp.json()
        state = content["state"]
        url = content["url"]
        state["handler"] = ""
        _ = session.put(url + "?force=true", json=state)

    success(f"All regions for tenant {tenant} now have no handler")


snapshots_app = Typer()

app.add_typer(snapshots_app, name="snapshots", help="Manage database snapshots")


@snapshots_app.command("list")
def list_snapshots(ctx: Context):
    """
    Get a list of snapshots for tenant
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.get(url + "/db/snapshots")
    if ctx.obj.output == "json":
        echo(resp.json())
        return

    lst = []
    headers = ["Name", "Timestamp", "Regions", "Objects"]
    for snapshot in resp.json()["snapshots"]:
        lst.append(
            [
                snapshot["name"],
                fmt_date(snapshot["timestamp"]),
                snapshot["counts"].get("regions"),
                snapshot["counts"].get("objects"),
            ]
        )

    echo(f"\nSnapshots available for tenant '{tenant}:")
    echo(tabulate(lst, headers=headers))


@snapshots_app.command("delete")
def delete_snapshot(
    ctx: Context,
    name: str = Argument(..., help="Name of the snapshot to delete"),
    y: bool = Option(False, is_flag=True, help="Override 'Are you sure' prompt"),
):
    """
    Delete a snapshot for tenant
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    if not y:
        confirm(
            f"Are you sure you want to delete snapshot '{name}' for the '{ctx.obj.tenant}' tenant?",
            abort=True,
        )
    try:
        _ = session.get(url + f"/db/snapshots/{name}")
        resp = session.delete(url + f"/db/snapshots/{name}")
    except ServerError as ex:
        abort(ex)
    success(f"Snapshot '{name}' has been deleted from tenant '{tenant}'")


@snapshots_app.command("create")
def create_snapshot(ctx: Context, name: str = Argument(..., help="Name of the snapshot to create")):
    """
    Create a snapshot for tenant from current state
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    data = {"name": name}
    try:
        resp = session.post(url + f"/db/snapshots", json=data)
    except ServerError as ex:
        abort(ex)
        print_table(resp.json())
    success(f"Snapshot '{name}' has been created for '{tenant}'")


@snapshots_app.command("restore")
def restore_snapshot(
    ctx: Context,
    name: str = Argument(..., help="Name of the snapshot to restore"),
    y: bool = Option(False, is_flag=True, help="Override 'Are you sure' prompt"),
):
    """
    Restore a snapshot to the current tenant, overriding the current database
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    if not y:
        confirm(
            f"Are you sure you want to restore snapshot '{name}' for the '{ctx.obj.tenant}' tenant?",
            abort=True,
        )

    try:
        _ = session.get(url + f"/db/snapshots/{name}")
        resp = session.post(url + f"/db/snapshots/{name}/restore")
    except ServerError as ex:
        abort(ex)
    success(f"Snapshot '{name}' has been restored for '{tenant}'")


@snapshots_app.command("delete-all")
def delete_all_snapshots(
    ctx: Context,
    y: bool = Option("...", is_flag=True, help="Override 'Are you sure' prompt"),
):
    """
    Delete all snapshots from tenant
    """
    session = ctx.obj.session
    tenant = ctx.obj.tenant
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = session.get(url + "/db/snapshots")
    snapshots = resp.json()["snapshots"]
    if not y:
        confirm(
            f"Are you sure you want to delete {len(snapshots)} snapshots for the '{ctx.obj.tenant}' tenant?",
            abort=True,
        )
    for snapshot in snapshots:
        name = snapshot["name"]
        try:
            resp = session.delete(url + f"/db/snapshots/{name}")
        except ServerError as ex:
            abort(ex)
    success(f"All {len(snapshots)} snapshots have been deleted from tenant '{tenant}'")
