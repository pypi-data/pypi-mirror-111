import sys
import os
import os.path
import traceback
from importlib import import_module

import requests

plugins = {}
commands = []


def load_plugins(path):
    """Load plugins by importing script modules from 'path'."""
    sys.path.insert(0, str(path))
    for modulename in os.listdir(path):
        if modulename.lower().endswith(".py") and not modulename.startswith("__"):
            pure_modulename, ext = os.path.splitext(modulename)
            print("Loading in plugin: {}".format(os.path.join(path, modulename)))
            try:
                _ = import_module(pure_modulename)
            except Exception:
                print("Error: Can't import module: {}".format(os.path.join(path, modulename)))
                traceback.print_exc()
                raise


def register(c):
    print("Registering class '{}' from module {}".format(c.__name__, c.__module__))
    plugins[c.get_name()] = c
    return c


def command(f):
    commands.append(f.__name__.replace("_", "-"))
    return f


@register
class KamoWorld(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.project: str = ctx.obj.project
        self.project_root: str = ctx.obj.project_root
        self.engine_root: str = ctx.obj.engine_root

        # Initialized by user
        self.auth_url: str = None
        self.auth_token: str = None
        self.kamo_url: str = None
        self.kamo_token: str = None
        self.tenant_name: str = None

        # Session variables
        self.session = None
        self.command_args = {}
        self.tenant = None
        self.db_url: str = None
        self.mq_url: str = None

    @classmethod
    def get_name(c):
        return c.__name__.lower()

    def get_kamorest(self):
        """Return a requests.Session object to a KamoREST endpoint. Do authentication if needed."""
        if self.session:
            return self.session

        session = requests.Session()
        session.timeout = 2.0
        self.kamo_url = self.kamo_url or "http://127.0.0.1:7000/"
        self.db_url = self.kamo_url + "db"
        self.mq_url = self.kamo_url + "mq"

        if not self.kamo_token and all([self.auth_url, self.auth_token]):
            ret = session.post(
                self.auth_url,
                data="grant_type=client_credentials",
                headers={
                    "Authorization": "Basic " + auth_token,
                    "Accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )

            ret.raise_for_status()
            resp = ret.json()

            self.kamo_token = resp["access_token"]
            self.token_expires_at_utc = utcnow() + resp["expires_in"]

        if self.kamo_token:
            session.auth = "Bearer " + self.kamo_token

        if self.tenant_name:
            session.headers["Kamo-Tenant"] = self.tenant_name

        self.session = session
        return self.session

    def get_kamotenant(self):
        if not self.tenant_name:
            raise RuntimeError("Tenant name must be specified!")
        self.get_kamorest()

        ret = self.session.get(self.kamo_url)
        ret.raise_for_status()
        self.tenant = ret.json()

        if not self.tenant:
            raise RuntimeError("Tenant {} not found at {}.".format(self.tenant_name, self.kamo_url))

        return self.session

    def _get_command(self, command):
        """Get member function that matches 'command' with dashes and whitespaces converted to underscore."""
        command = command.replace("-", "_").replace(" ", "_")
        fn = getattr(self, command, None)
        return fn

    def execute_command(self, command):
        fn = self._get_command(command)
        if not fn:
            raise RuntimeError("Command not found: {}".format(command))
        return fn()

    @command
    def list_commands(self):
        """List executable commands."""
        ret = []
        for command in commands:
            fn = self._get_command(command)
            if fn:
                entry = {}
                entry["name"] = command
                if fn.__doc__:
                    entry["description"] = fn.__doc__
                ret.append(entry)

        return {"commands": ret}

    @command
    def get_registry(self):
        raise RuntimeError("Not implemented yet")

    @command
    def get_world(self):
        """Returns all world info in a single json document."""
        s = self.get_kamotenant()

        resp = {}
        resp["tenant"] = self.tenant

        # Get all objects and group them by type
        groups = {}
        ret = s.get(self.db_url)
        ret.raise_for_status()
        for ob in ret.json()["objects"]:
            groups.setdefault(ob["object_type"], []).append(ob)
        resp["object_groups"] = groups

        return resp

    @command
    def create_tenant(self):
        """Create a new tenant. Specify 'tenant_name'."""
        if "tenant_name" not in self.command_args:
            raise RuntimeError("In create_tenant: 'tenant_name' must be specified in command args.")
        s = self.get_kamorest()
        ret = s.post(
            self.kamo_url + "api/",
            json={"name": self.command_args["tenant_name"], "db": "file", "mq": "file"},
        )
        ret.raise_for_status()
        return ret.json()
