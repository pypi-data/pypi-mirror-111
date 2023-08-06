import time
import sys
import kamocli
import os
import requests
import dateutil
from urllib.parse import urlparse, urljoin
from loguru import logger
import boto3
from io import BytesIO
import json
import botocore

from kamocli.utils import (
    dumps,
    abort,
    print_tab,
    fmt_date,
    check_tenant,
    print_table,
    out,
    success,
    get_builds_from_s3_url,
)
from kamosdk.exceptions import ServerError
from tabulate import tabulate

from typer import Typer, Context, Argument, Option, echo, secho, confirm

app = Typer()


@app.callback(
    help="Manage UE4 server builds",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def cli(ctx: Context):
    ctx.obj.tenant = ctx.obj.session.profile.tenant
    ctx.obj.builds_path = ctx.obj.session.profile.builds_path
    if not ctx.obj.builds_path and ctx.invoked_subcommand != "path":
        abort("Please set s3 build path with 'kamo builds path'")


@app.command("path")
def set_builds_path(
    ctx: Context,
    url: str = Argument(
        ..., help="Full s3 url to builds. e.g. s3://at-teamcity-artifacts/Existence/Existence_BuildServer/"
    ),
):
    if not url.startswith("s3://"):
        abort("S3 url must start with 's3://'")
    url = os.path.join(url, "")  # add trailing / if needed

    builds = get_builds_from_s3_url(url, num=1)
    if not builds:
        secho(f"No builds found in {url}.", fg="red")
        echo(f"This tool looks for subfolders containing 'buildinfo.json' which must at the very least have a 'version' key")
    else:
        echo(f"Builds found in path '{url}'. Adding to profile")
    ctx.obj.session.profile.builds_path = url


@app.command("list")
def list_builds(ctx: Context, num: int = Option(10, help="Number of the most recent builds to view")):
    """List server builds"""
    tenant = ctx.obj.session.profile.tenant
    builds = list(get_builds_from_s3_url(ctx.obj.builds_path, num).values())
    if ctx.obj.output == "json":
        echo(dumps(builds))
        return
    lst = []
    headers = ["Version", "Timestamp", "Branch", "S3 Path"]
    for build in builds:
        lst.append([build["version"], fmt_date(build.get("timestamp")), build.get("branch"), build["s3_path"]])
    echo(tabulate(lst, headers=headers))


@app.command("view")
def view_build(
    ctx: Context,
    version: str = Argument(..., help="Build version to view"),
    is_wait: bool = Option(
        False, "-w", "--wait", is_flag=True, help="Wait for the build to be ready if it is not found"
    ),
):

    """View details about a specific build"""
    tenant = ctx.obj.session.profile.tenant
    url = ctx.obj.session.knode_url + f"/builds/{tenant}/{version}"
    found = False

    if is_wait:
        start_time = time.time()
        while time.time() < start_time + 600.0:
            try:
                resp = ctx.obj.session.get(url)
                found = True
                break
            except ServerError as ex:
                out(f"Waiting for build {version}")
                time.sleep(10.0)
        if found:
            out(f"Build {version} is available", bold=True)
        else:
            out(f"Timeout waiting for build {version} to become available", fg="red")
            sys.exit(1)
    else:
        try:
            resp = ctx.obj.session.get(url)
        except ServerError as ex:
            abort(ex)

    content = resp.json()
    if ctx.obj.output == "json":
        print(dumps(content))
        return
    print_table(content["manifest"][0])


@app.command("delete")
def delete_build(
    ctx: Context,
    version: str = Argument(..., help="Build version to delete"),
    is_force: bool = Option(False, "-y", is_flag=True, help="Force a delete without a prompt"),
):
    """Delete a build"""
    tenant = ctx.obj.session.profile.tenant
    url = ctx.obj.session.knode_url + f"/builds/{tenant}/{version}"
    if not is_force:
        confirm(
            f"Are you sure you want to delete build '{version}' for the '{tenant}' tenant?",
            abort=True,
        )

    try:
        _ = ctx.obj.session.delete(url)
    except ServerError as ex:
        abort(ex)

    secho(f"Build {version} has been deleted for tenant {tenant}", bold=True)
