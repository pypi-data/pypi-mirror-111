import os, sys
import logging
import pathlib
import requests
import kamosdk
from kamosdk.session import ServiceSession
from kamosdk.exceptions import InvalidProfile
from kamocli.utils import dumps, out

from .utils import console_handler, abort

log = logging.getLogger(__name__)
help_string = """A utility for interfacing with Kamo dude"""

base_path = pathlib.Path(os.path.dirname(__file__))
commands_folder = base_path / "commands"


class ContextObj(object):
    def __init__(self):
        self.verbose = False
        self.profile_name = None
        self.home = os.getcwd()
        self.session = None
        self.service = None
        self.client = None
        self.base_path = base_path


from typer import Typer, Context, Argument, Option, echo, secho, confirm

app = Typer()


@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def cli(
    ctx: Context,
    verbose: str = Option(None, "-v", "--verbose", help="Verbose logging: info or debug"),
    profile: str = Option(None, "-p", "--profile", help="Profile name if you want to override the default profile"),
    output: str = Option("text", "-o", "--output", help="Output text or json"),
    tenant: str = Option(None, "-t", "--tenant", help="Override the tenant for this command"),
    domain: str = Option(None, "-d", "--domain", help="Override the domain for this command"),
):
    # by default we log out to console WARN and higher but can view info with -v
    # make sure this is called before importing the sdk so that we can grab all logging
    if verbose:
        console_handler.setLevel(getattr(logging, verbose.upper()))

    if ctx.obj is None:
        ctx.obj = ContextObj()
        ctx.obj.verbose = verbose
        ctx.obj.output = output
        try:
            ctx.obj.session = ServiceSession(profile=profile, tenant=tenant, domain=domain)
        except InvalidProfile as ex:
            log.debug(ex)
    try:
        out(
            f"Tenant: {ctx.obj.session.profile.tenant} - Profile: {ctx.obj.session.profile_name} - Endpoint: {ctx.obj.session.profile.domain}"
        )
    except:
        pass
    if ctx.invoked_subcommand not in ["tenants", "profile"]:
        if not ctx.obj.session:
            abort(f"You must create a profile with 'kamo profile add' to use this tool")

        if ctx.invoked_subcommand not in ["version"]:
            if not ctx.obj.session.profile.tenant:
                abort(f"You must select a tenant with 'kamo tenants' to use this tool")


@app.command()
def version(ctx: Context):
    """
    Show the versions of the CLI and all components
    """
    import kamocli

    ret = {"cli_version": kamocli.get_version_string()}
    ret["sdk_version"] = kamosdk.__version__
    ret["kamo_build_info"] = requests.get(ctx.obj.session.get_url("kamo")).json().get("build_info")
    ret["knode_build_info"] = requests.get(ctx.obj.session.get_url("knode")).json().get("build_info")

    if ctx.obj.output == "json" or 1:
        echo(dumps(ret))


from kamocli.commands import tenants, profile, login, db, nodes, builds, jobs, auth

app.add_typer(tenants.app, name="tenants", help="Manage tenants")
app.add_typer(profile.app, name="profile", help="Configure server profile to use")
app.add_typer(nodes.app, name="nodes", help="Manage EC2 instances")
app.add_typer(builds.app, name="builds")
app.add_typer(db.app, name="db")
app.add_typer(jobs.app, name="jobs")
