import json
import os


AIS_CACHE_FILE = "data/ais_cache.json"



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





def classify_ship(vessel):

    name = (
        vessel.get(
            "name",
            ""
        )
        .upper()
    )


    tanker_keywords = [

        "TANK",
        "OIL",
        "VLCC",
        "ULCC",
        "LNG",
        "LPG",
        "GAS",
        "CHEM",
        "PETRO",
        "CRUDE",
        "PRODUCT"

    ]


    container_keywords = [

        "MSC",
        "CMA",
        "MAERSK",
        "EVER",
        "COSCO"

    ]



    if any(
        key in name
        for key in tanker_keywords
    ):

        return "ناقلة"



    elif any(
        key in name
        for key in container_keywords
    ):

        return "حاويات"



    else:

        return "سفينة عامة"






def calculate_risk(vessels):


    report = {}



    for name, zone in CHOKEPOINTS.items():


        ships = []



        for vessel in vessels:


            if inside_zone(
                vessel,
                zone
            ):

                ships.append(
                    vessel
                )



        total = len(ships)


        tankers = 0
        containers = 0
        moving = 0
        stopped = 0



        for ship in ships:


            category = classify_ship(
                ship
            )



            if category == "ناقلة":

                tankers += 1



            elif category == "حاويات":

                containers += 1




            speed = ship.get(
                "speed",
                0
            )


            if speed is not None and speed < 1:

                stopped += 1

            else:

                moving += 1




        # =====================
        # حساب المؤشرات
        # =====================


        traffic_score = 0


        if total >= 30:

            traffic_score = 80

        elif total >= 15:

            traffic_score = 60

        elif total >= 5:

            traffic_score = 40

        elif total > 0:

            traffic_score = 20




        risk_score = traffic_score



        # ناقلات الطاقة

        risk_score += min(
            tankers * 5,
            20
        )



        # سفن متوقفة

        risk_score += min(
            stopped * 3,
            15
        )



        if risk_score >= 70:

            level = "مرتفع"


        elif risk_score >= 40:

            level = "متوسط"


        else:

            level = "منخفض"





        if risk_score >= 70:

            recommendation = (
                "رفع مستوى الجاهزية والمراقبة"
            )


        elif risk_score >= 40:

            recommendation = (
                "تعزيز المتابعة البحرية"
            )


        else:

            recommendation = (
                "استمرار المراقبة"
            )





        report[name] = {

            "عدد السفن":
                total,

            "ناقلات محتملة":
                tankers,

            "سفن حاويات":
                containers,

            "سفن متحركة":
                moving,

            "سفن متوقفة":
                stopped,

            "مؤشر الحركة":
                traffic_score,

            "درجة المخاطر":
                risk_score,

            "مستوى المخاطر":
                level,

            "التوصية":
                recommendation

        }




    return report






def analyze_maritime():

    vessels = load_vessels()

    return calculate_risk(
        vessels
    )
