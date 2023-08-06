import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from requests.exceptions import ConnectionError

from . import scopes as sc, utils
from .formatting import fprint, warning, fatal

try:
    scopes = sc.get_scope(sc.SCOPES)
except AssertionError:
    fatal("Invalid acces tokens given")
    exit(1)

os.makedirs(f"{os.environ['HOME']}/.spoclify", exist_ok=True)

try:
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scopes, redirect_uri="http://localhost", cache_path=f"{os.environ['HOME']}/.spoclify/.cache"))
except ConnectionError as error:
    fatal(f"No connection could be established: {str(error)}")
    exit(1)

utils.add_var("instance", sp)

def get_instance() -> spotipy.Spotify: return utils.get("instance", None)

def get_current_device(default_current = False):
    devices = sp.devices()

    if 'devices' in devices:
        for device in devices['devices']:
            if device['is_active']:
                id = device['id']
                if utils.get("current", "this will always be different") != id:
                    utils.add_var("current", id)
                return None if default_current else id
    warning("No devices currently active")
    return None