"""
utils
~~~~~~~~~~
Various utilities for kamo-sdk functionality.
"""

import jwt
import logging
from urllib.parse import urlsplit
import requests
from requests import codes
import binascii
import os
from importlib.util import find_spec
import boto3
import uuid

from .exceptions import ServerError, InvalidToken

log = logging.getLogger(__name__)


def decode_token(token):
    try:
        decoded_token = jwt.decode(token, algorithms=["RS256"], verify=False)
        return decoded_token
    except (KeyError, jwt.InvalidTokenError) as ex:
        raise InvalidToken(f"Token could not be decoded ({ex}): {token}")


def check_resp_error(resp):
    response_json = None
    try:
        resp.raise_for_status()
    except Exception:
        desc = resp.text
        try:
            response_json = resp.json()
            desc = response_json["error"]
            log.info(response_json)
        except Exception:
            pass
        if resp.status_code == 403:
            desc = f"API Key invalid. Please run 'kamo auth' ({resp.text})"

        if not desc:
            desc = "Status code %s received (%s)" % (resp.status_code, resp.text)
        else:
            desc += " (code %s)" % resp.status_code
        if resp.status_code >= 500:
            desc = "Server error in call to %s" % resp.url
            desc += " - Response headers: %s" % resp.headers
            desc += " - Response body: %s" % resp.text
            log.error(desc)
        else:
            log.info("Server error in call to %s", resp.url)

        error = ServerError(desc, url=resp.url, response=response_json)
        raise error from None


def get_access_token(api_key, client_id, oauth_url):
    """ """
    log.info("Fetching access token from Cognito")
    client = boto3.client("cognito-idp")
    result = client.initiate_auth(
        AuthFlow="REFRESH_TOKEN_AUTH", AuthParameters={"REFRESH_TOKEN": api_key}, ClientId=client_id
    )
    return result["AuthenticationResult"]["AccessToken"]


def host_from_url(host):
    """
    Gets the raw URI host of a url with trailing slash, no matter how it is formatted.

    For example, www.server.com/something -> https://www.server.com/
                 http://www.server.com -> http://www.server.com/
                 http://localhost:8080/something -> http://localhost:8080/

    """
    if "://" not in host:
        host = f"https://{host}"
    parts = urlsplit(host)
    return "{}://{}/".format(parts.scheme, parts.netloc)


def generate_kamo_id(class_name: str) -> str:
    guid = str(uuid.uuid4())
    if "." in class_name or class_name.lower() != class_name:
        raise RuntimeError(f"{class_name} not a valid kamo class name")

    return class_name + "." + guid[:8]
