import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPE = "user-read-currently-playing user-read-playback-state"

def get_client():
    return spotipy.Spotify(
        scope=SCOPE,
        client_id = os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri= os.getenv("SPOTIFY_REDIRECT_URI"),
        cache_path = ".spotify_cache",
    )

sp = get_client()

def current_song():
    try: 
        data = sp.currently_playing()

        if not data or not data.get("is_playing"):
            return None

        item = data.get("item")

        if not item:
            return None
        
        artist = item["artists"][0]["name"]
        track = item ["name"]

        return {
            "track": track,
            "artist": artist,
        }
    except Exception as e:
        print("Spotify error", e)
        return None