# intelligence/risk_engine.py

# المناطق الاستراتيجية البحرية

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
        "lat_min": 29.0,
        "lat_max": 32.8,
        "lon_min": 29.0
        "lon_max": 34.5
    }

}



def inside_area(lat, lon, area):

    return (
        area["lat_min"] <= lat <= area["lat_max"]
        and
        area["lon_min"] <= lon <= area["lon_max"]
    )




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



        count = len(detected)



        tankers = 0
        moving = 0
        stopped = 0



        for ship in detected:


            speed = ship.get("speed",0)


            if speed and speed > 1:
                moving += 1
            else:
                stopped += 1



            name_ship = ship.get(
                "name",
                ""
            ).upper()



            keywords = [
                "TANK",
                "OIL",
                "GAS",
                "VLCC",
                "CHEM",
                "PETRO"
            ]


            if any(
                k in name_ship
                for k in keywords
            ):
                tankers += 1



        score = 0



        # كثافة السفن

        if count >= 50:
            score += 40

        elif count >= 20:
            score += 30

        elif count >= 5:
            score += 20

        elif count > 0:
            score += 10



        # ناقلات

        score += min(
            tankers * 5,
            30
        )



        # الحركة

        if moving > 20:
            score += 20



        if score >= 70:

            level = "مرتفع"

            recommendation = (
                "رفع مستوى الجاهزية والمراقبة"
            )

        elif score >= 40:

            level = "متوسط"

            recommendation = (
                "زيادة المتابعة والتحليل"
            )

        else:

            level = "منخفض"

            recommendation = (
                "استمرار المراقبة"
            )



        report[name] = {


            "ships": count,

            "tankers": tankers,

            "moving": moving,

            "stopped": stopped,

            "risk_score": score,

            "risk_level": level,

            "recommendation": recommendation

        }



    return report
