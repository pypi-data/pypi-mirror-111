import requests
import logging

log = logging.getLogger(__name__)

from typer import Context, launch, echo, secho, Option, Typer, confirm, prompt

from kamocli.__main__ import app


@app.command("auth", help="Authenticate")
def cli(ctx: Context, api_key: str = Option(..., "-a", "--api-key", prompt="API Key")):
    domain = ctx.obj.session.profile.domain
    url = f"https://kamo.{domain}/.tenants"
    resp = None
    while not resp or resp.status_code == 403:
        if resp is not None:
            api_key = prompt("API Key incorrect. Please try again")
        echo(f"Testing {url} with API Key {api_key}...")
        resp = requests.get(url, timeout=2, headers={"Kamo-Api-Key": api_key})

    secho(f"API Key '{api_key}' has been added to current profile")
    ctx.obj.session.profile.api_key = api_key
