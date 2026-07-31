import json
import os


from intelligence.risk_engine import calculate_risk



AIS_CACHE_FILE = "data/ais_cache.json"





CHOKEPOINTS = {


    "مضيق هرمز": {

        "lat_min": 24,
        "lat_max": 28,
        "lon_min": 54,
        "lon_max": 58

    },


    "باب المندب": {

        "lat_min": 11,
        "lat_max": 14,
        "lon_min": 42,
        "lon_max": 45

    },


    "قناة السويس": {

        "lat_min": 29,
        "lat_max": 33,
        "lon_min": 31,
        "lon_max": 34

    }

}






def load_vessels():


    if not os.path.exists(
        AIS_CACHE_FILE
    ):

        return []



    with open(
        AIS_CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as f:


        return json.load(f)







def inside_zone(
    vessel,
    zone
):


    lat = vessel.get(
        "lat"
    )


    lon = vessel.get(
        "lon"
    )


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



            if inside_zone(
                vessel,
                zone
            ):

                detected.append(
                    vessel
                )





        risk = calculate_risk(
            detected,
            name
        )





        report[name] = risk





    return report
