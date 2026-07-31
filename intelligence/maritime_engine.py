import json
import os


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


    if not os.path.exists(AIS_CACHE_FILE):

        return []



    with open(
        AIS_CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)







def inside_zone(vessel, zone):


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







def classify_vessel(vessel):


    name = vessel.get(
        "name",
        ""
    ).upper()



    if any(
        x in name
        for x in [
            "TANK",
            "OIL",
            "GAS",
            "VLCC",
            "LNG",
            "CHEM"
        ]
    ):

        return "ناقلات"




    if any(
        x in name
        for x in [
            "MSC",
            "MAERSK",
            "CMA CGM",
            "COSCO",
            "HAPAG"
        ]
    ):

        return "حاويات"




    return "أخرى"








def calculate_risk(
    vessels,
    zone_name
):


    total = len(vessels)


    tankers = 0

    containers = 0

    moving = 0

    stopped = 0




    for vessel in vessels:


        category = classify_vessel(
            vessel
        )



        if category == "ناقلات":

            tankers += 1



        elif category == "حاويات":

            containers += 1




        speed = vessel.get(
            "speed",
            0
        )



        if speed and speed > 1:

            moving += 1

        else:

            stopped += 1






    score = 0



    # كثافة السفن

    if total >= 50:

        score += 35


    elif total >= 20:

        score += 25


    elif total >= 5:

        score += 10






    # سفن الطاقة

    score += min(
        tankers * 8,
        25
    )




    # التجارة

    score += min(
        containers * 3,
        15
    )




    # الحركة

    if moving > stopped:

        score += 10




    # التوقف

    if stopped >= 15:

        score += 15





    # أهمية المضيق

    if zone_name in [
        "مضيق هرمز",
        "قناة السويس"
    ]:

        score += 10



    elif zone_name == "باب المندب":

        score += 8





    score = min(
        score,
        100
    )





    if score >= 70:

        level = "مرتفع"

        recommendation = "رفع مستوى الجاهزية والمراقبة"



    elif score >= 40:

        level = "متوسط"

        recommendation = "تعزيز المتابعة"



    else:

        level = "منخفض"

        recommendation = "استمرار المراقبة"





    return {


        "السفن": total,

        "ناقلات": tankers,

        "حاويات": containers,

        "متحركة": moving,

        "متوقفة": stopped,

        "درجة": score,

        "المستوى": level,

        "التوصية": recommendation

    }









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




        report[name] = calculate_risk(
            detected,
            name
        )



    return report
