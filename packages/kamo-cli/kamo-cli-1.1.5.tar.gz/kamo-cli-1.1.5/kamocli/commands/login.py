import os
import sys

import requests
import logging
import http.server
import socketserver
import threading

from urllib.parse import urlparse, parse_qs

from kamosdk.config import get_profile_config, get_default_profile, create_profile
from kamocli.utils import abort, dumps

log = logging.getLogger(__name__)

from typer import Context, launch, echo, secho
from kamocli.__main__ import app


@app.command("login", help="Authenticate")
def cli(ctx: Context):
    raise NotImplementedError(
        "This functionality is currently not implemented. Please use 'kamo auth' and enter API Key"
    )
    PORT = 9898
    redirect_uri = f"http://localhost:{PORT}"

    profile = get_profile_config()
    root_info = ctx.obj.session.root_info

    client_id = root_info["config"]["auth_client_id"]
    cognito_url = root_info["config"]["auth_url"]
    url = f"{cognito_url}/login?client_id={client_id}&response_type=code&scope=email+openid+profile&redirect_uri={redirect_uri}"
    launch(url)

    httpd = None

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            query_components = parse_qs(urlparse(self.path).query)

            html = """
                <html>
                <head>
                <script>
                setTimeout("window.close();", 100);
                </script>
                </head>
                <body>
                <h1>You have been logged in</h1>
                <p>You can now close this window.</p>
                </body>
                </html>
                """

            self.wfile.write(bytes(html, "utf8"))

            # if we have a proper request, finish the song-and-dance
            # against keycloak and create the profile with the returned
            # refresh token (api key)
            if query_components:
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                data = {
                    "grant_type": "authorization_code",
                    "code": query_components["code"],
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                }
                url = f"{cognito_url}/oauth2/token"
                resp = requests.post(
                    url,
                    data=data,
                    headers=headers,
                )
                refresh_token = resp.json()["refresh_token"]
                create_profile(get_default_profile(), api_key=refresh_token, domain=profile["domain"])
                secho("You have been logged in", bold=True)

                # shut down the webserver in another thread to avoid deadlock
                threading.Thread(target=httpd.shutdown).start()

            return

    echo("Waiting for webpage...")
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", PORT), Handler)
    httpd.serve_forever()
    # Authentication flow will be completed in do_GET()
