import os
import requests
from urllib.parse import urlsplit, urljoin

from kamosdk.config import (
    root_config_folder,
    get_profiles,
    get_default_profile,
    set_default_profile,
    create_profile,
    delete_profile,
    clear_config,
)
from kamosdk.exceptions import InvalidProfile
from kamocli.utils import abort, dumps

from typer import Typer, Context, Argument, Option, echo, secho, confirm, prompt

app = Typer()


@app.command("list")
def list_profiles(ctx: Context):
    """lists all available profiles."""
    if ctx.obj.output == "json":
        echo(dumps(get_profiles()))
        return
    echo("Available profiles:")
    profiles = get_profiles()
    for profile_name in sorted(profiles):
        domain = profiles[profile_name]["domain"]
        col = ""
        if get_default_profile() == profile_name:
            col = "green"
            domain += " (selected)"
        secho(f"{profile_name:10} > {domain}", fg=col)
    echo("")


@app.command("current")
def current(ctx: Context):
    """displays content for the profile name."""
    if not get_profiles():
        abort("No profiles are currently set up. Please run 'kamo profile add [name]' to start")

    profile = ctx.obj.session.profile_name
    secho("Current profile: %s" % get_default_profile(), fg="green")
    profile_config = get_profiles().get(profile)
    if not profile_config:
        secho("Profile %s not found" % profile, fg="red")
        ctx.invoke(list)
        return

    for k, v in sorted(profile_config.items()):
        echo("   {0:20}{1}".format(k, v))
    echo("")


@app.command("view")
def view(ctx: Context, profile: str):
    """displays content for a given profile name."""
    if not get_profiles():
        abort("No profiles are currently set up. Please run 'kamo profile add [name]' to start")

    profile = (profile or "").lower()
    secho("Current profile: %s" % get_default_profile(), fg="green")
    profile_config = get_profiles().get(profile)
    if not profile_config:
        secho("Profile %s not found" % profile, fg="red")
        ctx.invoke(list)
        return

    echo("Viewing profile configuration for %s" % profile)
    for k, v in sorted(profile_config.items()):
        echo("   {0:20}{1}".format(k, v))
    echo("")


@app.command("set")
def set_profile(ctx: Context, profile: str):
    """sets the profile given by name as 'current'."""
    profile = profile.lower()
    try:
        set_default_profile(profile)
    except Exception as e:
        secho(str(e), fg="red")
        echo("View available profiles with 'kamo profile list'")
        return
    else:
        secho("Your profile has been changed to %s" % profile, bold=True)


@app.command("edit")
def edit_profile(ctx: Context):
    """open up the config.yaml file"""
    full_filename = os.path.join(root_config_folder, "config.yaml")
    echo("Editing config file located at %s" % (full_filename))

    echo("Modify your config and close the file")
    from click import edit

    edit(filename=full_filename, require_save=True)


@app.command("add")
def add_profile(
    ctx: Context,
    profile: str = Option(..., "-p", "--profile", prompt="What would you like to call this profile?"),
    domain: str = Option(..., "-d", "--domain", prompt="Domain name of the service (e.g. kamo.io)"),
    api_key: str = Option(..., "-k", "--api-key", prompt="API Key"),
    replace: bool = Option(False, "-r", "--replace", is_flag=True, help="Replace an existing profile"),
    tenant: str = Option(None, "-t", "--tenant", help="Default tenant (e.g. staging)"),
    skip_auth: str = Option(
        False, "-s", "--skip-auth", is_flag=True, help="Skip authentication (for local development)"
    ),
):
    """Creates a new profile of the specified name and allows you to configure it"""
    profile = profile.lower()
    if profile in get_profiles() and not replace:
        secho(
            "Profile '{}' already exists. Use --replace if you want to override it.".format(profile),
            fg="red",
        )
        return

    if "/" in domain:
        secho("Domain should only look like this: domain.io", fg="red")
        return

    if not skip_auth:
        url = f"https://kamo.{domain}/.tenants"
        try:
            resp = requests.get(url, timeout=2, headers={"Kamo-Api-Key": api_key})
            while resp.status_code == 403:
                api_key = prompt("API Key incorrect. Please try again")
                url = f"https://kamo.{domain}/.tenants"
                resp = requests.get(url, timeout=2, headers={"Kamo-Api-Key": api_key})

            resp.raise_for_status()
        except Exception as e:
            secho(f"{url} is not reachable: {e}", fg="red")
            if not confirm("Are you sure you want to add this domain?"):
                return

    try:
        create_profile(profile, api_key=api_key, domain=domain, skip_auth=skip_auth, tenant=tenant)
    except InvalidProfile as ex:
        abort(ex)
    set_default_profile(profile)
    echo("Profile has been added and is now active. If you want to edit it please run: kamo profile edit.")
    if not tenant:
        secho("Please select a tenant with 'kamo tenants list' / 'kamo tenants set'")


@app.command("delete")
def delete(ctx: Context, profile: str = Argument(..., help="Profile name to delete")):
    """accepts a profile name and deletes it."""
    profile = profile.lower()
    delete_profile(profile)
    secho("Profile '%s' has been deleted" % profile, bold=True)


@app.command("clear")
def delete(ctx: Context):
    """delete all profiles"""
    clear_config()
    secho("All profiles have been deleted and cache has been cleared. Please use 'kamo profile add' to get started", bold=True)
