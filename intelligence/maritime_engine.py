import json
import os


AIS_CACHE_FILE = "data/ais_cache.json"


CHOKEPOINTS = {

    "Strait of Hormuz": {
        "lat_min": 24,
        "lat_max": 28,
        "lon_min": 54,
        "lon_max": 57
    },

    "Bab el-Mandeb": {
        "lat_min": 11,
        "lat_max": 14,
        "lon_min": 42,
        "lon_max": 45
    },

    "Suez Canal": {
        "lat_min": 29,
        "lat_max": 32,
        "lon_min": 31,
        "lon_max": 33
    }

}



def load_vessels():

    if not os.path.exists(AIS_CACHE_FILE):
        return []

    with open(
        AIS_CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def check_zone(vessel, zone):

    lat = vessel.get("lat")
    lon = vessel.get("lon")

    if lat is None or lon is None:
        return False


    return (

        zone["lat_min"]
        <= lat
        <= zone["lat_max"]

        and

        zone["lon_min"]
        <= lon
        <= zone["lon_max"]

    )



def analyze_maritime():

    vessels = load_vessels()


    report = {}


    for name, zone in CHOKEPOINTS.items():

        detected = []


        for vessel in vessels:

            if check_zone(
                vessel,
                zone
            ):
                detected.append(vessel)



        risk_score = 0


        if len(detected) > 20:
            risk_score += 40

        elif len(detected) > 5:
            risk_score += 20



        report[name] = {

            "vessels": len(detected),

            "risk_score": risk_score,

            "risk_level":
                (
                    "HIGH"
                    if risk_score >= 70
                    else
                    "MEDIUM"
                    if risk_score >= 30
                    else
                    "LOW"
                )

        }


    return report
