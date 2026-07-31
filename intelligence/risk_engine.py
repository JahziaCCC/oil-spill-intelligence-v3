# intelligence/risk_engine.py

# محرك تقييم مخاطر المضائق البحرية


CHOKEPOINTS = {

    "مضيق هرمز": {

        "lat_min": 24.0,
        "lat_max": 28.0,
        "lon_min": 54.0,
        "lon_max": 58.0

    },


    "باب المندب": {

        "lat_min": 11.0,
        "lat_max": 14.0,
        "lon_min": 42.0,
        "lon_max": 45.0

    },


    "قناة السويس": {

        "lat_min": 29.0,
        "lat_max": 32.5,
        "lon_min": 31.0,
        "lon_max": 33.0

    }

}



def inside_area(lat, lon, area):

    return (

        area["lat_min"] <= lat <= area["lat_max"]

        and

        area["lon_min"] <= lon <= area["lon_max"]

    )





def calculate_risk(vessels):


    print()

    print("=" * 50)
    print("تشغيل محرك تحليل المخاطر البحرية")
    print("=" * 50)

    print("السفن الداخلة للتحليل:", len(vessels))


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





        ship_count = len(detected)


        tankers = 0
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




            ship_name = ship.get(
                "name",
                ""
            ).upper()



            tanker_keywords = [

                "TANK",
                "OIL",
                "GAS",
                "VLCC",
                "CHEM",
                "PETRO",
                "LNG"

            ]



            if any(
                word in ship_name
                for word in tanker_keywords
            ):

                tankers += 1





        # حساب درجة المخاطر

        score = 0



        # كثافة السفن

        if ship_count >= 50:

            score += 40

        elif ship_count >= 20:

            score += 30

        elif ship_count >= 10:

            score += 20

        elif ship_count > 0:

            score += 10




        # ناقلات استراتيجية

        score += min(
            tankers * 10,
            30
        )




        # مستوى الحركة

        if moving >= 20:

            score += 20

        elif moving >= 10:

            score += 10





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


            "ships": ship_count,

            "tankers": tankers,

            "moving": moving,

            "stopped": stopped,

            "risk_score": score,

            "risk_level": level,

            "recommendation": recommendation


        }





    return report
