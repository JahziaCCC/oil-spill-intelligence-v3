# intelligence/risk_engine.py

# Strategic Maritime Risk Engine V4


CHOKEPOINTS = {

    "مضيق هرمز": {
        "lat_min": 24.0,
        "lat_max": 28.0,
        "lon_min": 54.0,
        "lon_max": 58.0,
        "impact": "Energy HIGH"
    },


    "باب المندب": {
        "lat_min": 11.0,
        "lat_max": 14.0,
        "lon_min": 42.0,
        "lon_max": 45.0,
        "impact": "Trade HIGH"
    },


    "قناة السويس": {
        "lat_min": 29.0,
        "lat_max": 32.5,
        "lon_min": 31.0,
        "lon_max": 33.0,
        "impact": "Supply Chain HIGH"
    }

}



def inside_area(lat, lon, area):

    return (
        area["lat_min"] <= lat <= area["lat_max"]
        and
        area["lon_min"] <= lon <= area["lon_max"]
    )



def classify_ship(name):

    name = name.upper()

    tanker_words = [
        "TANK",
        "OIL",
        "VLCC",
        "LNG",
        "GAS",
        "CHEM",
        "PETRO"
    ]


    strategic_words = [
        "MSC",
        "MAERSK",
        "CMA",
        "EVER",
        "HAPAG",
        "COSCO",
        "ZIM"
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
                detected.append(vessel)



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


            if speed and speed > 1:
                moving += 1
            else:
                stopped += 1



            tanker, strategic_ship = classify_ship(
                ship.get("name","")
            )


            if tanker:
                tankers += 1


            if strategic_ship:
                strategic += 1




        movement_density = 0

        if ships:
            movement_density = round(
                (moving / ships) * 100,
                1
            )



        tanker_ratio = 0

        if ships:
            tanker_ratio = round(
                (tankers / ships) * 100,
                1
            )




        score = 0



        # كثافة السفن

        if ships >= 50:
            score += 40

        elif ships >= 25:
            score += 30

        elif ships >= 10:
            score += 20

        elif ships > 0:
            score += 10




        # ناقلات

        score += min(
            tankers * 10,
            30
        )



        # حركة

        if moving >= 20:
            score += 20

        elif moving >= 10:
            score += 10




        # سفن استراتيجية

        score += min(
            strategic * 5,
            10
        )



        if score >= 70:

            level = "مرتفع"
            readiness = "مرتفع"
            recommendation = (
                "رفع مستوى الجاهزية والمراقبة"
            )


        elif score >= 40:

            level = "متوسط"
            readiness = "متوسط"
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


            "ships": ships,

            "tankers": tankers,

            "strategic": strategic,

            "moving": moving,

            "stopped": stopped,

            "movement_density": movement_density,

            "tanker_ratio": tanker_ratio,

            "impact": area["impact"],

            "risk_score": score,

            "risk_level": level,

            "readiness": readiness,

            "recommendation": recommendation

        }



    return report
