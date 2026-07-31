import json
import os
from datetime import datetime


TRACK_FILE = "data/ais_tracks.json"


def load_tracks():

    if not os.path.exists(TRACK_FILE):
        return {}

    with open(TRACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save_tracks(data):

    os.makedirs("data", exist_ok=True)

    with open(
        TRACK_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



def update_track(vessels):

    tracks = load_tracks()


    for vessel in vessels:

        mmsi = str(vessel.get("mmsi"))

        if not mmsi or mmsi == "None":
            continue


        point = {

            "time":
                datetime.utcnow().isoformat(),

            "lat":
                vessel.get("lat"),

            "lon":
                vessel.get("lon"),

            "speed":
                vessel.get("speed"),

            "heading":
                vessel.get("heading"),

            "name":
                vessel.get("name")

        }


        if mmsi not in tracks:

            tracks[mmsi] = []


        tracks[mmsi].append(point)


        # الاحتفاظ بآخر 100 نقطة فقط
        tracks[mmsi] = tracks[mmsi][-100:]


    save_tracks(tracks)


    return tracks
