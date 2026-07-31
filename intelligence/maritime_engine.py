import json
import os


AIS_CACHE_FILE = "data/ais_cache.json"



# المناطق الاستراتيجية

CHOKEPOINTS = {

    "مضيق هرمز": {

        "lat_min": 22,
        "lat_max": 30,
        "lon_min": 50,
        "lon_max": 62

    },


    "باب المندب": {

        "lat_min": 8,
        "lat_max": 16,
        "lon_min": 38,
        "lon_max": 47

    },


    "قناة السويس": {

        "lat_min": 27,
        "lat_max": 33,
        "lon_min": 29,
        "lon_max": 35

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





def classify_ship(
    vessel
):

    name = (
        vessel
        .get("name","")
        .upper()
    )


    tanker_words = [

        "TANK",
        "OIL",
        "VLCC",
        "CHEM",
        "GAS",
        "LNG"

    ]


    container_words = [

        "MSC",
        "CMA",
        "MAERSK",
        "EVER"

    ]


    if any(
        x in name
        for x in tanker_words
    ):

        return "ناقلة"



    if any(
        x in name
        for x in container_words
    ):

        return "حاويات"



    return "سفينة عامة"






def calculate_risk(
    vessels
):


    report = {}



    for zone_name, zone in CHOKEPOINTS.items():


        detected = []


        for vessel in vessels:


            if inside_zone(
                vessel,
                zone
            ):

                detected.append(
                    vessel
                )



        count = len(
            detected
        )



        tankers = 0
        stopped = 0
        moving = 0



        for ship in detected:


            ship_type = classify_ship(
                ship
            )


            if ship_type == "ناقلة":

                tankers += 1



            speed = ship.get(
                "speed",
                0
            )


            if speed is not None and speed < 1:

                stopped += 1

            else:

                moving += 1




        # حساب مؤشر المخاطر


        score = 0



        # كثافة الحركة

        if count >= 30:

            score += 40

        elif count >= 10:

            score += 25

        elif count > 0:

            score += 10




        # ناقلات استراتيجية

        score += min(
            tankers * 5,
            30
        )



        # سفن متوقفة

        if stopped >= 5:

            score += 20

        elif stopped > 0:

            score += 10




        if score >= 70:

            level = "مرتفع"

        elif score >= 40:

            level = "متوسط"

        else:

            level = "منخفض"





        report[zone_name] = {


            "vessels":
                count,


            "tankers":
                tankers,


            "moving":
                moving,


            "stopped":
                stopped,


            "risk_score":
                score,


            "risk_level":
                level

        }



    return report






def analyze_maritime():

    vessels = load_vessels()


    return calculate_risk(
        vessels
    )
