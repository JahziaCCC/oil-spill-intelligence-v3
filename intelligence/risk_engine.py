# intelligence/risk_engine.py

# Strategic Maritime Risk Engine V5
# Chokepoint Early Warning Intelligence


CHOKEPOINTS = {


    "مضيق هرمز": {

        "strategic_importance": "Energy HIGH",

        "center": (26.0, 56.5),

        "lat_range": 4.0,

        "lon_range": 4.0,

        "proximity": 3.0,

        "weight": 1.5

    },


    "باب المندب": {

        "strategic_importance": "Trade HIGH",

        "center": (12.8, 43.5),

        "lat_range": 3.0,

        "lon_range": 3.0,

        "proximity": 2.5,

        "weight": 1.4

    },


    "قناة السويس": {

        "strategic_importance": "Supply Chain HIGH",

        "center": (31.0, 32.3),

        "lat_range": 3.0,

        "lon_range": 2.0,

        "proximity": 2.0,

        "weight": 1.2

    }

}





def distance_zone(
        lat,
        lon,
        area,
        factor=1
):

    center_lat, center_lon = area["center"]


    return (

        abs(lat - center_lat)
        <=
        area["lat_range"] * factor

        and

        abs(lon - center_lon)
        <=
        area["lon_range"] * factor

    )






def vessel_class(name):

    name = name.upper()


    tanker_words = [

        "TANK",
        "OIL",
        "PETRO",
        "CHEM",
        "LNG",
        "GAS",
        "VLCC"

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



    for name, area in CHOKEPOINTS.items():


        inside = []

        nearby = []



        for vessel in vessels:


            lat = vessel.get("lat")

            lon = vessel.get("lon")


            if lat is None or lon is None:

                continue



            if distance_zone(
                lat,
                lon,
                area,
                1
            ):

                inside.append(
                    vessel
                )


            elif distance_zone(
                lat,
                lon,
                area,
                area["proximity"]
            ):

                nearby.append(
                    vessel
                )





        ships = len(inside)

        nearby_count = len(nearby)



        tankers = 0

        strategic = 0

        moving = 0

        stopped = 0




        analyzed = inside + nearby



        for ship in analyzed:


            speed = ship.get(
                "speed",
                0
            )


            if speed > 1:

                moving += 1

            else:

                stopped += 1



            tanker, strategic_ship = vessel_class(
                ship.get(
                    "name",
                    ""
                )
            )


            if tanker:

                tankers += 1



            if strategic_ship:

                strategic += 1






        traffic_density = 0


        if analyzed:

            traffic_density = round(
                (moving / len(analyzed))
                *
                100,
                1
            )





        score = 0



        # السفن داخل المنطقة

        if ships >= 50:

            score += 35

        elif ships >= 20:

            score += 25

        elif ships >= 10:

            score += 15

        elif ships > 0:

            score += 10





        # السفن القريبة (إنذار مبكر)

        if nearby_count >= 20:

            score += 20

        elif nearby_count >= 10:

            score += 10

        elif nearby_count > 0:

            score += 5





        # ناقلات النفط

        score += min(
            tankers * 12,
            30
        )





        # سفن استراتيجية

        score += min(
            strategic * 8,
            25
        )






        # الحركة

        if moving >= 20:

            score += 15

        elif moving >= 10:

            score += 8






        score = int(
            score *
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





        report[name] = {


            "strategic_importance":
                area["strategic_importance"],


            "ships":
                ships,


            "nearby_ships":
                nearby_count,


            "tankers":
                tankers,


            "strategic":
                strategic,


            "moving":
                moving,


            "stopped":
                stopped,


            "traffic_density":
                traffic_density,


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
