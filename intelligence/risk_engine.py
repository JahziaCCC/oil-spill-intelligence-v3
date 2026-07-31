# intelligence/risk_engine.py

# محرك تقييم مخاطر المضائق البحرية
# Strategic Maritime Risk Engine


CHOKEPOINTS = {

    "مضيق هرمز": {

        "lat_min": 24.0,
        "lat_max": 28.0,
        "lon_min": 54.0,
        "lon_max": 58.0,

        "strategic_importance": "Energy HIGH"

    },


    "باب المندب": {

        "lat_min": 11.0,
        "lat_max": 14.0,
        "lon_min": 42.0,
        "lon_max": 45.0,

        "strategic_importance": "Trade HIGH"

    },


    "قناة السويس": {

        "lat_min": 29.0,
        "lat_max": 32.5,
        "lon_min": 31.0,
        "lon_max": 33.0,

        "strategic_importance": "Supply Chain HIGH"

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





        ship_count = len(detected)


        tankers = 0

        strategic_ships = 0

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



            strategic_keywords = [

                "MSC",
                "MAERSK",
                "CMA",
                "EVER",
                "COSCO",
                "HAPAG",
                "ONE"

            ]




            if any(
                word in ship_name
                for word in tanker_keywords
            ):

                tankers += 1




            if any(
                word in ship_name
                for word in strategic_keywords
            ):

                strategic_ships += 1





        # =========================
        # مؤشرات الحركة
        # =========================


        if ship_count > 0:

            traffic_density = round(
                (moving / ship_count) * 100,
                1
            )

        else:

            traffic_density = 0





        if ship_count > 0:

            tanker_ratio = round(
                (tankers / ship_count) * 100,
                1
            )

        else:

            tanker_ratio = 0





        # =========================
        # حساب درجة المخاطر
        # =========================


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





        # ناقلات النفط

        score += min(
            tankers * 10,
            30
        )





        # سفن استراتيجية

        score += min(
            strategic_ships * 5,
            20
        )





        # الحركة

        if moving >= 20:

            score += 20


        elif moving >= 10:

            score += 10





        # =========================
        # مستوى الخطر
        # =========================


        if score >= 70:


            level = "مرتفع"

            readiness = "حرج"

            recommendation = (
                "رفع مستوى الجاهزية والمراقبة"
            )



        elif score >= 40:


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

                area.get(
                    "strategic_importance",
                    "N/A"
                ),


            "ships":

                ship_count,


            "tankers":

                tankers,


            "strategic":

                strategic_ships,


            "moving":

                moving,


            "stopped":

                stopped,


            "traffic_density":

                traffic_density,


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
