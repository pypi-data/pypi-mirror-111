"""
KamoEd - Kamo Editor CLI Tool

A Command Line Interface for dispatching KamoEd plugin commands.
"""
import sys
import os.path
import traceback
import tempfile
import json
from functools import wraps
from contextlib import contextmanager

import click
import requests

from kamocli.ed import kamoplugin


class JsonResponser(click.Group):
    """
    Turn return values from commands into json formatted response.
    Catch any exceptions and pretty print as json as well.
    """

    def invoke(self, ctx):
        ctx.obj.json = {}
        ctx.obj.json["_command"] = sys.argv
        ctx.obj.json["success"] = False

        try:
            ret = super(JsonResponser, self).invoke(ctx)
            if ret:
                ctx.obj.json.update(ret)
            ctx.obj.json["success"] = True

        except click.exceptions.Exit as e:
            pass
        except requests.exceptions.HTTPError as e:
            ctx.obj.json = {
                "status_code": e.response.status_code,
                "error": e.response.json().get("error", e.response.text),
                "request": "{} {}".format(e.request.method, e.request.url),
            }
            traceback.print_exc()
        finally:
            if getattr(ctx.obj, "stdout", None):
                print("----BEGIN JSON-----")
                print(json.dumps(ctx.obj.json, indent=4))
                print("----END JSON-----")
            else:
                with tempfile.TemporaryFile(mode="w", delete=False) as f:
                    print("JSON result file: {}".format(f.name))
                    json.dump(ctx.obj.json, f, indent=4)


@click.group(cls=JsonResponser, context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--project", help="Name of the project")
@click.option("--project-root", help="Project root path")
@click.option("--engine-root", help="Engine root path")
@click.option("--plugin", help="Name of plugin class. Default is 'kamoworld'")
@click.option("--data", type=click.File(mode="r"), help="Path to input data json file.")
@click.option(
    "--include",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    multiple=True,
    help="Path to plugins folder. Multiple include options are supported.",
)
@click.option("--stdout", is_flag=True, help="Write result to stdout instead of tempfile.")
@click.pass_context
def cli(ctx, project, project_root, engine_root, plugin, data, include, stdout):
    """KamoEd - Unreal Engine Kamo Editor Extension."""
    print(ctx.obj.base_path)
    ctx.obj.project = project
    ctx.obj.project_root = project_root
    ctx.obj.engine_root = engine_root
    ctx.obj.plugin = plugin
    ctx.obj.include = include
    ctx.obj.stdout = stdout

    if data:
        ctx.obj.data = json.load(data)
    else:
        ctx.obj.data = {}

    path = ctx.obj.base_path / "ed" / "coreplugins"
    kamoplugin.load_plugins(path)

    for path in ctx.obj.include:
        kamoplugin.load_plugins(path)


@cli.command()
@click.pass_context
def info(ctx):
    """Get information on this command line tool."""
    return {"plugins": list(kamoplugin.plugins)}


@cli.command()
@click.pass_context
@click.option("--auth_url", help="OAuth2 endpoint for authorization.")
@click.option("--auth_token", help="OAuth2 token for authorization.")
@click.option("--kamo_registry_url", help="KamoRegistry endpoint.")
@click.option("--kamo_url", help="KamoREST endpoint.")
@click.option("--kamo_token", help="KamoRegistry/REST authorization token.")
@click.option("--tenant", help="KamoREST tenant to use.", default="default")
@click.option("--docker-local-server", help="Build and use a local image for the server.")
@click.argument("command")
def wc(
    ctx,
    auth_url,
    auth_token,
    kamo_registry_url,
    kamo_url,
    kamo_token,
    tenant,
    docker_local_server,
    command,
):
    """
    Execute a world command.

    Run 'list-commands' to get a list of available commands.

    An instance of KamoWorld is created and a command is executed on the world.
    The result is formatted as a json document and written to a temporary file. The name of the file
    is displayed in the output.
    """

    def trailing_slash(url):
        if not url or url.endswith("/"):
            return url
        else:
            return url + "/"

    ctx.obj.auth_url = auth_url
    ctx.obj.auth_token = auth_token
    ctx.obj.kamo_registry_url = trailing_slash(kamo_registry_url)
    ctx.obj.kamo_url = trailing_slash(kamo_url)
    ctx.obj.kamo_token = kamo_token
    ctx.obj.tenant = tenant
    ctx.obj.docker_local_server = docker_local_server

    plugin = ctx.obj.plugin or "kamoworld"  # The default plugin
    if plugin not in kamoplugin.plugins:
        raise RuntimeError("No plugin named '{}' found! Plugins: {}".format(plugin, list(kamoplugin.plugins)))

    world_class = kamoplugin.plugins[plugin]
    world = world_class(ctx)

    # Assign user values
    world.auth_url = ctx.obj.auth_url
    world.auth_token = ctx.obj.auth_token
    world.kamo_url = ctx.obj.kamo_url
    world.kamo_token = ctx.obj.kamo_token
    world.tenant_name = ctx.obj.tenant
    world.docker_local_server = True

    # Assign session values
    world.command_args = ctx.obj.data

    print(">> Executing '{}' in plugin {}".format(command, world.__class__))

    ret = world.execute_command(command)

    return ret
