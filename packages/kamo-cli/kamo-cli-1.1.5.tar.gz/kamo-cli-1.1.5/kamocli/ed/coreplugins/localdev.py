import os
import os.path
import sys
import subprocess
import shutil
import pathlib
import webbrowser
from psutil import process_iter, NoSuchProcess, AccessDenied
import signal

from kamocli.ed.kamoplugin import KamoWorld, register, command


def kill_process_by_id(ports):
    # Start by killing the backend if its running
    for proc in process_iter():
        try:
            connections = proc.connections(kind="inet")
        except AccessDenied:
            continue  # Skipping processes that we don't have access to

        for con in connections:
            if con.laddr.port in ports:
                print(f"Killing Kamo backend on port: {con.laddr.port}")
                try:
                    proc.send_signal(signal.SIGTERM)
                except NoSuchProcess:
                    print("Process already killed")
                except AccessDenied:
                    print("Ignoring an access denied error")


@register
class LocalDev(KamoWorld):
    def __init__(self, ctx):
        super().__init__(ctx)

    @command
    def update_backend(self):
        backend_url = "git@github.com:kamo-io/kamo-platform.git"

        project_root = pathlib.Path(self.project_root).resolve().parent
        backend_root = project_root.joinpath("kamo-platform")

        print(project_root)
        if not backend_root.exists():

            # clone the project from git
            print("Cloning the backend for first time use")
            subprocess.call("git clone " + backend_url, cwd=project_root.as_posix(), shell=True)
            subprocess.call("pipenv install --dev", cwd=backend_root.as_posix(), shell=True)
            return

        else:
            print("Killing the backend if its already running")
            ports_to_kill = [7000, 7001, 7002]
            kill_process_by_id(ports_to_kill)

            print("Pulling latest...")
            subprocess.call("git pull", cwd=backend_root.as_posix(), shell=True)
            return

    @command
    def start_local_backend(self):
        ports_to_kill = [7000, 7001, 7002]
        kill_process_by_id(ports_to_kill)
        # This is hardcoded for demo's,  need to find a smarter way to start the backend through KamoED
        backend_root = pathlib.Path(self.project_root).resolve().parent.joinpath("kamo-platform")

        subprocess.Popen("start pipenv run kamoregistry", cwd=backend_root.as_posix(), shell=True)
        subprocess.Popen("start pipenv run kamorest", cwd=backend_root.as_posix(), shell=True)
        subprocess.Popen("start pipenv run knode jobs process -d", cwd=backend_root.as_posix(), shell=True)

    @command
    def open_kamoflage(self):
        """Open the kamo frontend locally"""
        webbrowser.open("https://app-vikingworld.kamo.io/", new=0, autoraise=True)

    @command
    def open_knode_web(self):
        """Open the kamo frontend locally"""
        webbrowser.open("https://app-vikingworld.kamo.io/", new=0, autoraise=True)

    @command
    def open_knode_logs(self):

        path = os.path.join(os.path.expanduser("~"), ".kamo", "knode_logs")

        if not os.path.exists(path):
            print(f"Path not found: {path}")
        else:
            if sys.platform == "win32":
                cmd = f'explorer /root, "{path}"'
            elif sys.platform == "darwin":
                cmd = ["open", "-R", path]
            else:
                print(f"Attempting to run on unsupported platform {sys.platform}")
                print(f"Point your file exploring application to: {path}")
                cmd = None

            if cmd:
                print(f"executing: {cmd}")
                subprocess.call(cmd)

    @command
    def open_local_db(self):

        path = os.path.join(os.path.expanduser("~"), ".kamo", self.project, "db")

        if not os.path.exists(path):
            print(f"Path not found: {path}")
        else:
            if sys.platform == "win32":
                cmd = f'explorer /root, "{path}"'
            elif sys.platform == "darwin":
                cmd = ["open", "-R", path]
            else:
                print(f"Attempting to run on unsupported platform {sys.platform}")
                print(f"Point your file exploring application to: {path}")
                cmd = None

            if cmd:
                print(f"executing: {cmd}")
                subprocess.call(cmd)

    @command
    def start_servers(self):
        """starts unreal dedicated server processes through the editor with uncooked content"""

        use_debug = self.ctx.obj.data["useDebug"]
        should_wait_for_debugger = self.ctx.obj.data["waitForDebugger"]
        overwrite_regions = self.ctx.obj.data["regionOverwrite"]

        log_cmds = self.ctx.obj.data["logCmds"]
        cmd_args = self.ctx.obj.data["cmdArgs"]
        cmd_args = [arg.strip() for arg in list(filter(None, cmd_args.split(",")))] + [f"-LogCmds={log_cmds}"]

        project_root = pathlib.Path(self.project_root).resolve()
        uproject_file = project_root.joinpath(self.project).as_posix() + ".uproject"

        engine_root = pathlib.Path(self.engine_root)

        if sys.platform == "win32":
            extention = ".exe"
            platform = "Win64"

        # Create the engine path
        executable_name = "ue4editor"

        if use_debug:
            executable_name = executable_name + "-Win64-DebugGame"

        if sys.platform == "darwin":
            if use_debug:
                executable_name = "UE4Editor-Mac-DebugGame.app/Contents/MacOS/UE4Editor-Mac-DebugGame"
            else:
                executable_name = "UE4Editor.app/Contents/MacOS/UE4Editor"

        editor_path = engine_root.joinpath("Binaries", platform, executable_name)

        if extention:
            editor_path = editor_path.as_posix() + extention

        # Get the region names from the database
        regions = []

        if overwrite_regions:
            regions = overwrite_regions.split(" ")
        else:
            session = self.get_kamotenant()
            db_path = self.db_url

            res = session.get(db_path, params={"object_type": "root"})
            res.raise_for_status()

            for each_root_object in res.json()["objects"]:
                region_name = each_root_object["id"]
                regions.append(region_name)

        base_port = 8000
        for i, region_name in enumerate(regions):
            port = str(base_port + i)

            cmd = [
                editor_path,
                uproject_file,
                "-log",
                "-server",
                f"-port={port}",
                "-KamoAllowCreateRegion",
                f"-regions={region_name}",
                f"LOG={region_name}.log",
                *cmd_args,
            ]

            if should_wait_for_debugger:
                cmd.append("-WaitForDebugger")

            subprocess.Popen(cmd)

    @command
    def delete_tenant(self):
        """delete world database"""
        path = os.path.join(os.path.expanduser("~"), ".kamo", self.project)

        if not os.path.exists(path):
            print(f"No tenant found: {path}")
            return

        shutil.rmtree(path)

    @command
    def restore_db_template(self):
        """restores the database from a template"""
        db_path = os.path.join(os.path.expanduser("~"), ".kamo", self.project, "db")

        # Hardcoded kamo ED path:
        kamoExtentions = f"{self.project_root}\KamoEdExtensions\db_templates"
        template_name = self.ctx.obj.data["template"]

        target_path = os.path.join(kamoExtentions, template_name)
        if not os.path.exists(target_path):
            print(f"Unable to find database template at :{target_path}")
            return

        # Delete the world database before applying the template
        self.delete_tenant()
        shutil.copytree(target_path, db_path)
