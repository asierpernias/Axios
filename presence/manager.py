import time

from presence.spotify import current_song
from presence.slack import set_status

def loop():
    last= ""

    while True:
        song = current_song()

        if song != last:
            last = song

            if song:
                set_status(song)
            else: 
                set_status("Available", ":robot_face")
        time.sleep(30)