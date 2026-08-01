# intelligence/risk_engine.py

# Strategic Maritime Risk Engine V3.1
# Baseline + Confidence + Early Warning


CHOKEPOINTS = {

    "مضيق هرمز": {

        "lat_min": 24.0,
        "lat_max": 28.0,
        "lon_min": 54.0,
        "lon_max": 58.0,

        "strategic_importance": "Energy HIGH",

        "baseline_ships": 15
    },


    "باب المندب": {

        "lat_min": 11.0,
        "lat_max": 14.0,
        "lon_min": 42.0,
        "lon_max": 45.0,

        "strategic_importance": "Trade HIGH",

        "baseline_ships": 15
    },


    "قناة السويس": {

        "lat_min": 29.0,
        "lat_max": 32.5,
        "lon_min": 31.0,
        "lon_max": 33.0,

        "strategic_importance": "Supply Chain HIGH",

        "baseline_ships": 22
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
                "ONE"

            ]



            if any(
                x in ship_name
                for x in tanker_keywords
            ):

                tankers += 1



            if any(
                x in ship_name
                for x in strategic_keywords
            ):

                strategic += 1




        # ======================
        # المؤشرات
        # ======================


        traffic_density = 0

        if ship_count:

            traffic_density = round(
                (moving / ship_count) * 100,
                1
            )



        stopped_ratio = 0

        if ship_count:

            stopped_ratio = round(
                (stopped / ship_count) * 100,
                1
            )



        baseline = area["baseline_ships"]


        deviation = 0

        if baseline:

            deviation = round(
                ((ship_count - baseline)
                / baseline) * 100,
                1
            )



        # ======================
        # Risk Score
        # ======================


        score = 0



        # كثافة السفن

        if ship_count >= baseline * 2:

            score += 40

        elif ship_count >= baseline:

            score += 25

        elif ship_count > 0:

            score += 10




        # ناقلات

        score += min(
            tankers * 10,
            20
        )



        # سفن استراتيجية

        score += min(
            strategic * 8,
            20
        )



        # توقف ملاحي

        if stopped_ratio >= 70:

            score += 20

        elif stopped_ratio >= 50:

            score += 10




        score = min(
            score,
            100
        )



        # ======================
        # Confidence
        # ======================


        confidence = 50


        if ship_count > 0:

            confidence += 15


        if tankers > 0:

            confidence += 10


        if strategic > 0:

            confidence += 10


        if stopped_ratio > 50:

            confidence += 10



        confidence = min(
            confidence,
            95
        )




        # ======================
        # Alert
        # ======================


        reasons = []


        if ship_count >= baseline:

            reasons.append(
                "كثافة سفن أعلى من المعدل"
            )


        if stopped_ratio >= 50:

            reasons.append(
                "ارتفاع نسبة السفن المتوقفة"
            )


        if tankers:

            reasons.append(
                "وجود ناقلات نفط"
            )


        if strategic:

            reasons.append(
                "وجود سفن استراتيجية"
            )




        if score >= 80:

            alert = "🔴 RED ALERT"
            level = "مرتفع"

        elif score >= 50:

            alert = "🟠 WARNING"
            level = "متوسط"

        else:

            alert = "🟢 NORMAL"
            level = "منخفض"




        report[name] = {


            "strategic_importance":
                area["strategic_importance"],


            "ships":
                ship_count,


            "baseline":
                baseline,


            "deviation":
                deviation,


            "tankers":
                tankers,


            "strategic":
                strategic,


            "moving":
                moving,


            "stopped":
                stopped,


            "stopped_ratio":
                stopped_ratio,


            "traffic_density":
                traffic_density,


            "risk_score":
                score,


            "confidence":
                confidence,


            "alert":
                alert,


            "alert_reasons":
                reasons,


            "risk_level":
                level,


            "readiness":
                "مرتفع"
                if score >=50
                else "منخفض",


            "recommendation":

                "رفع مستوى الجاهزية التشغيلية"
                if score >=80

                else

                "زيادة المتابعة والتحليل"
                if score >=50

                else

                "استمرار المراقبة"

        }



    return report
