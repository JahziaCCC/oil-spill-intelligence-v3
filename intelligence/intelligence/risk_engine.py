# intelligence/risk_engine.py

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
            "HAPAG",
            "COSCO"
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





    # ناقلات الطاقة

    score += min(
        tankers * 8,
        25
    )



    # سفن الحاويات

    score += min(
        containers * 3,
        15
    )




    # حركة السفن

    if moving > stopped:

        score += 10



    # التوقف داخل المنطقة

    if stopped >= 15:

        score += 15





    # أهمية المضيق

    if zone_name == "مضيق هرمز":

        score += 10



    elif zone_name == "باب المندب":

        score += 8



    elif zone_name == "قناة السويس":

        score += 10





    if score >= 70:

        level = "مرتفع"



    elif score >= 40:

        level = "متوسط"



    else:

        level = "منخفض"






    if level == "مرتفع":

        recommendation = "رفع مستوى الجاهزية والمراقبة"

    elif level == "متوسط":

        recommendation = "تعزيز المتابعة"

    else:

        recommendation = "استمرار المراقبة"






    return {


        "السفن":
            total,


        "ناقلات":
            tankers,


        "حاويات":
            containers,


        "متحركة":
            moving,


        "متوقفة":
            stopped,


        "درجة":
            min(score,100),


        "المستوى":
            level,


        "التوصية":
            recommendation

    }
