"""
session
~~~~~~~~~~
Service Session, low-level object for communicating with RESTFul services.
"""

import requests
import requests.utils
from requests import codes
from os import environ
import copy
import json
import platform
import time
import logging
from hashlib import sha1
from typing import Optional, Union, Dict, List

from . import __version__
from .exceptions import ServerError, ServiceNotFound, InvalidProfile
from .utils import check_resp_error, get_access_token
from .config import Config, load_cache, save_cache, save_config

log = logging.getLogger(__name__)

config = Config()


class Profile:

    profile_name = None
    content = None

    def __init__(self, profile_name: Optional[str] = None, content: Optional[Dict] = None) -> None:
        if profile_name:
            self.profile_name = profile_name
            self.content = config.get("profiles")[self.profile_name]
        else:
            self.profile_name = None
            self.content = content

    def __getattr__(self, name):
        if name in self.content:
            return self.content[name]
        return None

    def __setattr__(self, name, value):
        if name in ("profile_name", "content"):
            super(Profile, self).__setattr__(name, value)
        else:
            self.content[name] = value
            if self.profile_name:
                save_config()


class ServiceSession(requests.Session):
    """
    A wrapped requests session object with base_url and endpoints
    from kamo service api's
    """

    def __init__(self, domain=None, api_key=None, profile=None, tenant=None, *args, **kwargs):
        super(ServiceSession, self).__init__(*args, **kwargs)
        # retry idempotent methods up to 5 times
        # if not environ.get("KAMO_DISABLE_RETRY"):
        #     retries = 5
        #     backoff_factor = 0.5
        #     status_forcelist = (500, 502, 503, 504)
        #     retry = Retry(
        #         total=retries,
        #         read=retries,
        #         connect=retries,
        #         backoff_factor=backoff_factor,
        #         status_forcelist=status_forcelist,
        #     )
        #     adapter = HTTPAdapter(max_retries=retry)
        #     self.mount("http://", adapter)
        #     self.mount("https://", adapter)

        # if no named profile or api key is passed in
        if not profile and not api_key:
            # find the default profile, if any
            if environ.get("KAMO_PROFILE"):
                profile = environ["KAMO_PROFILE"]
                log.info("Using profile '%s' from environment", profile)
            else:
                profile = config.get("default_profile")
                if profile:
                    log.info("Using default profile '%s' from config", profile)

        self.profile_name = profile

        # if we have a profile we will load it from the config
        if self.profile_name:
            log.info(
                "Initializing client with profile '%s'. Available profiles: %s",
                self.profile_name,
                list(config.get("profiles")),
            )
            if self.profile_name not in config.get("profiles"):
                raise InvalidProfile("The config profile (%s) could not be found" % profile)
            self.profile = Profile(self.profile_name)
        else:
            # if there is no profile there needs to be configuration set in the
            # environment, in which case we create an ephemeral profile, not
            # backed up by disk.
            api_key = api_key or environ.get("KAMO_API_KEY")
            if not api_key:
                raise InvalidProfile("No profile specified and KAMO_API_KEY not set in environment")
            domain = domain or environ.get("KAMO_DOMAIN")
            self.profile = Profile(content={"api_key": api_key, "domain": domain, "tenant": ""})

        self.root_info = {}
        self.endpoints = {}
        self.token = None

        if environ.get("KAMO_DOMAIN", domain):
            domain = environ.get("KAMO_DOMAIN", domain)
            log.info(f"Overriding domain with {domain}")
            self.profile.domain = domain
        if environ.get("KAMO_TENANT", tenant):
            tenant = environ.get("KAMO_TENANT", tenant)
            log.info(f"Overriding tenant with {tenant}")
            self.profile.tenant = tenant

        self.domain = self.profile.domain
        self.api_key = self.profile.api_key
        if domain:
            self.domain = domain
        if api_key:
            self.api_key = api_key

        if environ.get("KAMO_API_KEY"):
            log.info("Overriding api key from environment")
            self.api_key = environ["KAMO_API_KEY"]

        self.cache_name = sha1((self.domain or "").encode()).hexdigest()
        self.user_agent = "Kamo-SDK/%s Python/%s %s/%s" % (
            __version__,
            platform.python_version(),
            platform.system(),
            platform.release(),
        )

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
            "Kamo-Tenant": self.profile.tenant,
            "Kamo-Api-Key": self.api_key,
        }

        if not self._load():
            self._initialize()

        self.endpoints = self.root_info.get("endpoints")

    def _initialize(self) -> None:
        try:
            self.fetch_root_info()
        except ServerError:
            log.warning("Error fetching root info")


    def _save(self) -> None:
        contents = {
            "token": self.token,
            "root_info": self.root_info,
            "api_key": self.api_key,
        }
        save_cache(self.cache_name, contents)

    def _load(self) -> bool:
        contents = load_cache(self.cache_name)
        if not contents:
            return False
        self.token = contents["token"]
        self.root_info = contents["root_info"]
        if self.token:
            self.headers["Authorization"] = "Bearer {}".format(self.token)
        return True

    def _do_request(self, method, retry=True, *args, **kwargs):

        # method: GET
        old_content_type = self.headers["Content-Type"]
        if "headers" in kwargs:
            self.headers.update(kwargs["headers"])

        if method == "get":
            # ! Temporary hack: Remove the application/json content-type header for GET's
            del self.headers["Content-Type"]

        try:
            st = time.time()
            response = getattr(super(ServiceSession, self), method)(*args, **kwargs)
            diff = time.time() - st
        finally:
            self.headers["Content-Type"] = old_content_type

        # Manage response from the server
        log.info("%s %s returned %s in %.3f sec" % (method.upper(), args[0], response.status_code, diff))

        check_resp_error(response)
        return response

    def get_url(self, subdomain):
        if self.profile.urls:
            return self.profile.urls[subdomain]
        else:
            return f"https://{subdomain}.{self.domain}"

    @property
    def kamo_url(self):
        return self.get_url("kamo")

    @property
    def knode_url(self):
        return self.get_url("knode")

    def get(self, *args, **kw):
        return self._do_request("get", True, *args, **kw)

    def put(self, *args, **kw):
        return self._do_request("put", True, *args, **kw)

    def post(self, *args, **kw):
        return self._do_request("post", True, *args, **kw)

    def delete(self, *args, **kw):
        return self._do_request("delete", True, *args, **kw)

    def fetch_root_info(self) -> Dict:
        log.debug("fetch_root_info(): domain: {0}, headers: {1}".format(self.domain, self.headers))
        root_url = self.get_url("kamo")
        try:
            r = requests.get(root_url, timeout=3.0, headers=self.headers)
        except requests.exceptions.ConnectionError as ex:
            raise ServerError(f"Could not reach server {root_url} ({ex})") from None
        except requests.exceptions.ReadTimeout as ex:
            raise ServerError(f"Could not reach server {root_url} ({ex})") from None

        r.raise_for_status()

        if "application/json" not in r.headers["Content-Type"]:
            raise ServerError("Unexpected response: %s" % r.text, url=root_url) from None
        ret = r.json()
        self.root_info = ret
        return ret

    def url_from_endpoint(self, endpoint: str) -> str:
        try:
            return self.endpoints[endpoint]
        except KeyError:
            raise ServerError(
                "Endpoint '%s' is not exported by '%s'.\nAvailable endpoints are %s"
                % (endpoint, self.root_url, ", ".join(self.endpoints.keys()))
            )

    def request(self, method, url, **kwargs):
        log.debug("Calling %s %s %s", method, url, repr(kwargs))
        stripped_headers = copy.copy(self.headers)
        if "Authorization" in stripped_headers:
            stripped_headers["Authorization"] = "Bearer ***"
        log.debug("Headers: %s" % json.dumps(stripped_headers))
        if "json" in kwargs:
            log.debug("Payload:\n%s" % json.dumps(kwargs["json"], indent=4))
        return super(ServiceSession, self).request(method, url, **kwargs)

    def links(self, resp: Dict) -> Dict:
        return resp.get("links", {})
