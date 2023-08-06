import click
import logging
import kamocli
import requests

from kamocli.utils import dumps, abort, success, print_table
from kamosdk.exceptions import ServerError

log = logging.getLogger(__name__)

from typer import Typer, Context, Argument, Option, echo, secho, confirm

app = Typer()


@app.command("list")
def list_tenants(ctx: Context):
    """
    List available tenants on the server
    """
    resp = ctx.obj.session.get(ctx.obj.session.kamo_url + "/.tenants")
    resp.raise_for_status()
    content = resp.json()
    if ctx.obj.output == "json":
        echo(dumps(content))
        return

    if not content.get("tenants"):
        abort("No tenants found")

    tenant = ctx.obj.session.profile.tenant or "(none)"
    secho(f"Currently selected tenant: " + click.style(tenant, bold=True) + "\nAvailable tenants:")
    for tenant in content["tenants"]:
        print_table(tenant)
        echo("")


@app.command("set")
def set_tenant(ctx: Context, tenant_name):
    """
    Pick a tenant to use for tenant-specific commands
    """
    tenant_name = tenant_name.lower()
    if not ctx.obj.session:
        abort("No profile found. Please add a profile with kamo profile add")
    resp = ctx.obj.session.get(ctx.obj.session.kamo_url + "/.tenants")
    resp.raise_for_status()
    content = resp.json()
    if not content.get("tenants"):
        abort("No tenants found on server")

    tenants = set()
    for t in content["tenants"]:
        tenants.add(t["name"].lower())
    if tenant_name not in tenants:
        abort("Invalid tenant. Please choose from: {}".format(", ".join(tenants)))

    ctx.obj.session.profile.tenant = tenant_name
    success("Tenant has been set to: {}".format(tenant_name), bold=True)


@app.command("create")
def create_tenant(ctx: Context, tenant_name: str):
    """
    Create a new tenant
    """
    tenant_name = tenant_name.lower()
    try:
        _ = ctx.obj.session.get(ctx.obj.session.kamo_url + f"/.tenants/{tenant_name}")
        abort(f"Tenant {tenant_name} already exists")
    except ServerError:
        pass
    data = {"name": tenant_name}

    _ = ctx.obj.session.post(ctx.obj.session.kamo_url + "/.tenants", json=data)
    success(f"Tenant {tenant_name} has been created.", bold=True)


@app.command("delete")
def delete_tenant(
    ctx: Context,
    tenant_name: str,
    is_force: bool = Option(False, "-y", is_flag=True, help="Delete the tenant without a prompt"),
):
    """
    Delete a tenant
    """
    tenant_name = tenant_name.lower()
    try:
        _ = ctx.obj.session.get(ctx.obj.session.kamo_url + f"/.tenants/{tenant_name}")
        abort(f"Tenant {tenant_name} already exists")
    except ServerError:
        pass
    if not is_force:
        confirm(
            f"Are you sure you want to permanently delete the tenant '{tenant_name}'?",
            abort=True,
        )

    _ = ctx.obj.session.delete(ctx.obj.session.kamo_url + f"/.tenants/{tenant_name}")
    success(f"Tenant {tenant_name} has been permanently deleted.", bold=True)
