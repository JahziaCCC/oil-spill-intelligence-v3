import json
import os
from datetime import datetime


TRACK_FILE = "data/vessel_tracks.json"



def load_tracks():

    if not os.path.exists(TRACK_FILE):

        return {}


    with open(
        TRACK_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)





def save_tracks(tracks):

    os.makedirs(
        "data",
        exist_ok=True
    )


    with open(
        TRACK_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            tracks,
            f,
            ensure_ascii=False,
            indent=4
        )






def calculate_direction(
    old_lat,
    old_lon,
    new_lat,
    new_lon
):


    if old_lat is None or old_lon is None:

        return "رصد أولي"



    lat_change = new_lat - old_lat
    lon_change = new_lon - old_lon



    if abs(lat_change) < 0.01 and abs(lon_change) < 0.01:

        return "ثابتة"



    if lat_change > 0:

        north = "شمال"

    else:

        north = "جنوب"




    if lon_change > 0:

        east = "شرق"

    else:

        east = "غرب"



    return north + " " + east






def update_vessel_tracks(
    vessels
):


    tracks = load_tracks()



    updated = []



    for vessel in vessels:


        mmsi = str(
            vessel.get(
                "mmsi"
            )
        )


        if not mmsi:

            continue



        old = tracks.get(
            mmsi,
            {}
        )



        direction = calculate_direction(

            old.get("lat"),

            old.get("lon"),

            vessel.get("lat"),

            vessel.get("lon")

        )



        record = {


            "mmsi":
                mmsi,


            "name":
                vessel.get(
                    "name",
                    ""
                ),


            "lat":
                vessel.get(
                    "lat"
                ),


            "lon":
                vessel.get(
                    "lon"
                ),


            "speed":
                vessel.get(
                    "speed",
                    0
                ),


            "direction":
                direction,


            "last_update":
                datetime.utcnow()
                .isoformat()

        }



        tracks[mmsi] = record


        updated.append(
            record
        )



    save_tracks(
        tracks
    )



    return updated
