"""
config
~~~~~~~~~~
Configuration, caching and profile management for kamo cli.

"""

import os
import logging
import yaml
import json
import time
from pathlib import Path
from typing import Dict, Tuple, Sequence, Optional
import shutil


from .exceptions import InvalidProfile

root_config_folder = Path(os.path.expanduser("~/.kamo"))
CONFIG_FILENAME = "config.yaml"

log = logging.getLogger(__name__)

DEFAULT_PROFILE_NAME = "default"
CACHE_SECONDS = 600


def load_cache(name: str) -> Optional[Dict]:
    """
    Load a dictionary from disk cache by name.

    The file is found in ~/.kamo/cache/[name].cache and is assumed to be a
    dictionary in json format.

    If KAMO_DISABLE_CACHE environment variable is non-zero this method does nothing
    """
    if os.environ.get("KAMO_DISABLE_CACHE"):
        return None
    cache_file = root_config_folder.joinpath("cache", name + ".cache")
    try:
        file_age = time.time() - os.path.getmtime(cache_file)
        if file_age > CACHE_SECONDS:
            log.info("Cache is too old, removing it.")
            os.remove(cache_file)
            raise FileNotFoundError

        contents = json.load(cache_file.open("r"))
        log.info("Loaded contents from cache %s", cache_file)
        return contents
    except FileNotFoundError:
        pass
    except Exception:
        log.exception("Could not load from cache %s", cache_file)
    return None


def save_cache(name: str, contents: Dict) -> None:
    if os.environ.get("KAMO_DISABLE_CACHE"):
        return
    try:
        cache_folder = root_config_folder.joinpath("cache")
        os.makedirs(cache_folder, exist_ok=True)
        cache_file = root_config_folder.joinpath(cache_folder, name + ".cache")
        json.dump(contents, cache_file.open("w"), default=str)
        log.info("Dumped contents into cache %s", cache_file)
    except Exception:
        log.exception("Could not save cache %s", cache_file)


def clear_cache() -> None:
    cache_folder = root_config_folder.joinpath("cache")
    try:
        shutil.rmtree(cache_folder)
    except FileNotFoundError:
        pass


class Config:
    """
    Borg pattern Config class see:
    http://code.activestate.com/recipes/66531-singleton-we-dont-need-no-stinkin-singleton-the-bo/

    Example usage:

    >>> config = Config({'my': 'config'})
    """

    shared_state: Dict = {}
    data: Dict = {}

    def __init__(self, data: Optional[Dict] = None):
        self.__dict__ = self.shared_state
        self.set(data)

    def dict(self) -> Dict:
        return self.data

    def set(self, data: Optional[Dict]) -> None:
        if data is None:
            data = {}
        self.data.update(data)

    def get(self, key: str, default=None):
        return self.data.get(key, default)


def _load_config() -> Dict:
    config_file = root_config_folder.joinpath(CONFIG_FILENAME)
    try:
        content = yaml.safe_load(config_file.open())
        if not isinstance(content, dict):
            raise Exception("Invalid config")
        return content
    except Exception:
        log.info("Config file not found or invalid")
    return {}


def save_config() -> None:
    config = Config()
    config_filename = root_config_folder.joinpath(CONFIG_FILENAME)
    os.makedirs(root_config_folder, exist_ok=True)
    with config_filename.open("w") as conf_file:
        yaml.safe_dump(config.dict(), conf_file)


def clear_config() -> None:
    root_config_folder.joinpath(CONFIG_FILENAME).unlink(missing_ok=True)
    try:
        root_config_folder.joinpath("cache").rmdir()
    except:
        pass

def _init_config() -> None:
    config = Config()
    config.set({"default_profile": None, "profiles": []})
    content = _load_config()
    if "profiles" not in content:
        content["profiles"] = {}
    for name, profile in content["profiles"].copy().items():
        if not _is_profile_valid(profile):
            log.warning("Profile '%s' is invalid and will be ignored", name)
            del content["profiles"][name]
            break

    config.set(content)


def _is_profile_valid(profile):
    required_keys = ["api_key", "domain"]
    for k in required_keys:
        if k not in profile:
            log.error(f"Profile {profile} is invalid since it does not contain required key {k}")
            return False
    return True


def create_profile(name: str, api_key: str, domain: Optional[str] = None, skip_auth: bool = False, tenant: Optional[str] = None) -> None:
    """
    Create a new profile from api key and persist to disk

    :param name: Unique name of the profile for referencing later
    :param api_key: API Key from keycloak for the server
    :param domain: domain of the server. If not set, the url from the api key is used
    :param skip_auth: Do not use authentication (local development)
    :param tenant: Set a default tenant (optional)
    :raises: InvalidProfile

    """
    urls = {"knode": f"https://knode.{domain}", "kamo": f"https://kamo.{domain}"}
    profile: Dict = {"api_key": api_key, "domain": domain, "urls": urls}
    if skip_auth:
        profile["skip_auth"] = True
    if tenant:
        profile["tenant"] = tenant
    if not _is_profile_valid(profile):
        raise InvalidProfile("Profile is missing required keys")
    config = Config()
    profiles = config.get("profiles")
    profiles[name] = profile
    config.set({"profiles": profiles})
    save_config()


def delete_profile(name: str) -> None:
    config = Config()
    profiles = get_profiles()
    if name not in profiles:
        raise InvalidProfile("Profile does not exist")
    if config.get("default_profile") == name:
        config.set({"default_profile": None})
    del profiles[name]
    save_config()


def set_default_profile(name: str) -> None:
    """
    Set a named profile as the default one if no profile is specified

    :param name: Name of the profile
    :raises: InvalidProfile
    """
    config = Config()
    if name not in config.get("profiles"):
        raise InvalidProfile("Profile does not exist")
    config.set({"default_profile": name})
    save_config()


def get_profiles() -> Dict:
    config = Config()
    return config.get("profiles")


def get_default_profile() -> Optional[str]:
    config = Config()
    return os.environ.get("KAMO_PROFILE") or config.get("default_profile")


def get_config() -> Dict:
    config = Config()
    return config.data


def get_profile_config() -> Dict:
    config = Config()
    try:
        return config.data["profiles"][get_default_profile()]
    except KeyError:
        raise InvalidProfile("No current profile found")


_init_config()
