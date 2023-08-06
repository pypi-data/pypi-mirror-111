#!/usr/bin/env python

import botocore.session
import click
import typer
import configparser
import logging
import os
import sys
import json
from jsonpath_rw import parse
import yaml
import dateutil
from functools import wraps, cmp_to_key
from kamosdk.exceptions import ServerError
from urllib.parse import urlparse, urljoin
import boto3
from io import BytesIO
import json
import botocore
from loguru import logger
from operator import attrgetter, itemgetter

log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.WARN)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(console_handler)

log = logging.getLogger(__name__)


def print_error(*txt):
    color_print(*txt, color="red")


def print_warn(*txt):
    color_print(*txt, color="yellow")


def print_success(*txt):
    color_print(*txt, color="green")


def color_print(*args, **kwargs):
    color = kwargs.get("color", "reset")
    for x in args:
        typer.echo(typer.style(x, fg=color))


def print_tab(key, val):
    val_txt = val
    if isinstance(val, dict):
        val_txt = ", ".join([f"{k}={v}" for k, v in val.items()])
    val = typer.style(str(val_txt), bold=True)
    typer.echo("{0:20}{1}".format(key, val))


def print_table(obj):
    try:
        for k, v in obj.items():
            print_tab(k, v)
    except Exception:
        typer.echo(obj)


def dumps(obj):
    try:
        return json.dumps(obj, indent=4, sort_keys=True)
    except Exception:
        return repr(obj)


def output_pretty_json(dct, keys):
    ret = ""
    for k in keys:
        jsonpath_expr = parse(k)
        ret = [match.value for match in jsonpath_expr.find(dct)]
        lst = [""]
        if ret:
            if isinstance(ret[0], list) or isinstance(ret[0], dict):
                lst = yaml.dump(ret[0]).split("\n")
            else:
                lst = [str(ret[0])]
        print_tab(k.split(".")[-1], lst[0])
        if len(lst) > 1:
            for v in lst[1:]:
                print_tab("", v)


def find_aws_credentials(profile):
    """
    Returns the aws credentials for the specified profile.
    If no profile is passed in, returns the credentials for the currently selected profile

    Args:
        profile name

    Returns:
        Dict containing at least aws_access_key_id, aws_secret_access_key

    Raises:
        RuntimeError is no default profile or the named profile was not found

    """
    if not profile:
        access_key = None
        secret_key = None
        token = ""
        credentials = botocore.session.get_session().get_credentials()
        if credentials:
            access_key = credentials.access_key
            secret_key = credentials.secret_key
            token = getattr(credentials, "token") or ""
        if not access_key or not secret_key:
            raise RuntimeError("No Default AWS profile set")

        return {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "aws_session_token": token,
        }

    folder = os.path.join(os.path.expanduser("~"), ".aws")
    filename = os.path.join(folder, "credentials")
    cfg = configparser.ConfigParser()
    with open(filename) as fp:
        cfg.readfp(fp)
        ret = {}
        if profile not in cfg:
            raise RuntimeError("No AWS profile '%s' found in %s" % (profile, filename))
        for key in cfg[profile]:
            ret[key] = cfg[profile][key]
    return ret


def abort(reason, code=1):
    """
    exit with non-zero exit code and write reason for error to stderr.
    If we are outside a typer context and exception will be raised instead
    """
    ctx = click.get_current_context(silent=True)
    if not ctx:
        raise Exception(f"Abnormal Termination: {reason}")

    if ctx.obj and ctx.obj.output == "json":
        ret = {"success": False, "exit_code": code, "message": str(reason)}
        typer.echo(json.dumps(ret))
    else:
        typer.echo(typer.style(str(reason), fg="red"), file=sys.stderr)
    sys.exit(code)


def out(txt, **kw):
    ctx = click.get_current_context(silent=True)
    if ctx and ctx.obj and ctx.obj.output == "json":
        log.info(txt)
    else:
        typer.secho(txt, **kw)


def success(reason, response=None, **kw):
    ctx = click.get_current_context(silent=True)
    if not ctx:
        print(reason)

    exit_code = 0
    if ctx.obj and ctx.obj.output == "json":
        ret = {
            "success": True,
            "exit_code": exit_code,
            "message": str(reason),
            "response": response,
        }
        typer.echo(json.dumps(ret))
    else:
        if not kw:
            kw = {"fg": "white", "bold": True}
        typer.secho(str(reason), **kw)
    sys.exit(exit_code)


def check_profile(ctx):
    if not ctx.obj.client:
        abort("You have no active profile or selected profile is invalid. Run 'kamo profile add [name]'")


def fmt_date(dt: str):
    try:
        return dateutil.parser.parse(dt).strftime("%Y-%m-%d %H:%M")
    except:
        return dt


def check_tenant(func):
    @wraps(func)
    def _check(*args, **kwargs):
        ctx = click.get_current_context()
        tenant = ctx.obj.session.profile.tenant
        if not tenant:
            abort("Before using this command please set a tenant by running: kamo tenants set [name]")
        else:
            return func(*args, **kwargs)

    return _check


def get_tenant_url(session, tenant):
    url = session.kamo_url + f"/{tenant}"
    return url


def find_regions(ctx):
    url = get_tenant_url(ctx.obj.session, ctx.obj.tenant)
    resp = ctx.obj.session.get(url + "/db/regions?start=0&end=100")
    ret = set()
    for region in resp.json()["regions"]:
        ret.add(region["id"])
    return ret


def find_builds(ctx):
    tenant = ctx.obj.session.profile.tenant
    url = ctx.obj.session.knode_url + f"/builds/{tenant}"
    resp = ctx.obj.session.get(url)
    ret = []
    for build in resp.json()["builds"]:
        ret.append(build["version"])
    return ret


def find_nodes(ctx):
    url = ctx.obj.session.knode_url + f"/nodes"
    resp = ctx.obj.session.get(url)
    resp.raise_for_status()
    ret = {}
    for node in resp.json():
        ret[node["node_id"]] = node
    return ret


def format_region_name(map_name: str, volume_name: str = None, instance_id: str = None):
    region_name = "region." + map_name
    if volume_name:
        region_name += "^" + volume_name
    if instance_id:
        instance_id += "#" + instance_id
    return region_name.lower()


def parse_region_name(region_name):
    volume_name = instance_id = None
    region_name = region_name.replace("region.", "")
    if "#" in region_name:
        region_name, instance_id = region_name.split("#")
    if "^" in region_name:
        region_name, volume_name = region_name.split("^")
    return region_name, volume_name, instance_id


def get_builds_from_s3_url(url, num=10):
    buildinfo_filename = "buildinfo.json"
    parts = urlparse(url)
    bucket_name = parts.netloc
    path = parts.path[1:]
    logger.debug("Finding builds in bucket {}, path {}", bucket_name, path)

    client = boto3.client("s3")
    s3 = boto3.resource("s3")
    paginator = client.get_paginator("list_objects")
    paths = []
    try:
        for result in paginator.paginate(Bucket=bucket_name, Prefix=path, Delimiter="/"):
            folders = [f["Prefix"] for f in result.get("CommonPrefixes", [])]
            paths.extend(folders)
    except botocore.exceptions.ClientError as e:
        if "AccessDenied" in repr(e):
            abort(f"You do not have access to {bucket_name}. Please review your AWS credentials")
    paths.sort(reverse=True)
    builds = []
    for p in paths:
        key = urljoin(p, buildinfo_filename)
        obj = s3.Object(bucket_name, key)
        f = BytesIO()
        try:
            obj.download_fileobj(f)
        except botocore.exceptions.ClientError:
            # most likely not found
            continue
        f.seek(0)
        c = json.load(f)
        s3_path = f"s3://{bucket_name}/{p}"
        c["s3_path"] = s3_path
        v = c.get("version", "")
        if len(v.split(".")) < 3:
            logger.warning("Buildinfo file in {} has an invalid version {} and is excluded", s3_path, v)
            continue
        builds.append(c)
        if len(builds) >= num:
            break
    versions = {}

    def mycmp(a, b):
        va = a["version"].split("-")[0]
        vb = b["version"].split("-")[0]
        if va > vb:
            return 1
        elif vb > va:
            return -1
        else:
            if a["timestamp"] > b["timestamp"]:
                return 1
            else:
                return -1

    builds.sort(key=cmp_to_key(mycmp), reverse=True)
    for build in builds:
        versions[build["version"]] = build
    return versions
