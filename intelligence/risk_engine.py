# intelligence/risk_engine.py

# Strategic Maritime Risk Engine V4
# Geospatial Chokepoint Intelligence


CHOKEPOINTS = {


    "مضيق هرمز": {

        "strategic_importance": "Energy HIGH",

        # نطاق تقريبي للمضيق
        "polygon": [

            (24.2, 56.0),
            (24.2, 58.0),
            (27.0, 58.0),
            (27.0, 56.0)

        ],

        "weight": 1.5

    },



    "باب المندب": {

        "strategic_importance": "Trade HIGH",

        "polygon": [

            (12.0, 42.0),
            (12.0, 44.8),
            (13.8, 44.8),
            (13.8, 42.0)

        ],

        "weight": 1.3

    },



    "قناة السويس": {

        "strategic_importance": "Supply Chain HIGH",

        "polygon": [

            (29.0, 32.0),
            (29.0, 33.2),
            (32.5, 33.2),
            (32.5, 31.0)

        ],

        "weight": 1.2

    }

}




def inside_area(lat, lon, area):

    points = area["polygon"]


    latitudes = [
        p[0]
        for p in points
    ]


    longitudes = [
        p[1]
        for p in points
    ]


    return (

        min(latitudes)
        <=
        lat
        <=
        max(latitudes)

        and

        min(longitudes)
        <=
        lon
        <=
        max(longitudes)

    )





def vessel_type(name):

    name = name.upper()


    tanker_words = [

        "TANK",
        "OIL",
        "GAS",
        "VLCC",
        "LNG",
        "CHEM",
        "PETRO"

    ]


    strategic_words = [

        "MSC",
        "MAERSK",
        "CMA",
        "COSCO",
        "EVER",
        "ONE",
        "HAPAG"

    ]


    tanker = any(
        x in name
        for x in tanker_words
    )


    strategic = any(
        x in name
        for x in strategic_words
    )


    return tanker, strategic





def calculate_risk(vessels):


    report = {}



    for area_name, area in CHOKEPOINTS.items():


        detected = []



        for vessel in vessels:


            lat = vessel.get("lat")
            lon = vessel.get("lon")


            if lat is None or lon is None:

                continue



            if inside_area(
                lat,
                lon,
                area
            ):

                detected.append(
                    vessel
                )




        ships = len(detected)


        tankers = 0
        strategic = 0
        moving = 0
        stopped = 0



        for ship in detected:


            speed = ship.get(
                "speed",
                0
            )


            if speed > 1:

                moving += 1

            else:

                stopped += 1



            name = ship.get(
                "name",
                ""
            )


            tanker, strategic_ship = vessel_type(
                name
            )


            if tanker:

                tankers += 1


            if strategic_ship:

                strategic += 1




        traffic = 0

        if ships:

            traffic = round(
                (moving / ships) * 100,
                1
            )



        tanker_ratio = 0

        if ships:

            tanker_ratio = round(
                (tankers / ships) * 100,
                1
            )




        # =========================
        # Risk Score V4
        # =========================


        score = 0



        # كثافة السفن

        if ships >= 50:

            score += 35

        elif ships >= 20:

            score += 25

        elif ships >= 10:

            score += 15

        elif ships > 0:

            score += 5




        # ناقلات النفط

        score += min(
            tankers * 12,
            30
        )



        # سفن استراتيجية

        score += min(
            strategic * 8,
            20
        )



        # الحركة

        if moving >= 20:

            score += 15

        elif moving >= 10:

            score += 8



        # أهمية المضيق

        score = int(
            score
            *
            area["weight"]
        )



        if score > 100:

            score = 100





        if score >= 75:

            level = "مرتفع"

            readiness = "حرج"

            recommendation = (
                "رفع مستوى الجاهزية والمراقبة"
            )


        elif score >= 50:

            level = "متوسط"

            readiness = "مرتفع"

            recommendation = (
                "زيادة المتابعة والتحليل"
            )


        else:

            level = "منخفض"

            readiness = "منخفض"

            recommendation = (
                "استمرار المراقبة"
            )





        report[area_name] = {


            "strategic_importance":
                area["strategic_importance"],


            "ships":
                ships,


            "tankers":
                tankers,


            "strategic":
                strategic,


            "moving":
                moving,


            "stopped":
                stopped,


            "traffic_density":
                traffic,


            "tanker_ratio":
                tanker_ratio,


            "risk_score":
                score,


            "risk_level":
                level,


            "readiness":
                readiness,


            "recommendation":
                recommendation


        }



    return report
