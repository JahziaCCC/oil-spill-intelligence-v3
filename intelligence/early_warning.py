# intelligence/early_warning.py

# Strategic Maritime Early Warning Engine V7


def generate_warning(risk_report):


    warnings = {}



    for area, data in risk_report.items():


        score = data.get(
            "risk_score",
            0
        )


        reasons = []



        if data.get(
            "ships",
            0
        ) >= 20:

            reasons.append(
                "كثافة سفن عالية"
            )



        if data.get(
            "nearby_ships",
            0
        ) >= 10:

            reasons.append(
                "وجود سفن قريبة من منطقة الاختناق"
            )



        if data.get(
            "stopped",
            0
        ) >= 10:

            reasons.append(
                "ازدحام أو توقف ملاحي"
            )



        if data.get(
            "tankers",
            0
        ) > 0:

            reasons.append(
                "وجود ناقلات نفط"
            )



        if data.get(
            "strategic",
            0
        ) > 0:

            reasons.append(
                "وجود سفن استراتيجية"
            )






        if score >= 75:

            level = "🔴 RED ALERT"

            action = (
                "رفع مستوى الجاهزية التشغيلية الفورية"
            )



        elif score >= 50:

            level = "🟠 ORANGE ALERT"

            action = (
                "زيادة المتابعة ورفع مستوى الاستعداد"
            )



        elif score >= 25:

            level = "🟡 YELLOW ALERT"

            action = (
                "مراقبة مستمرة"
            )



        else:

            level = "🟢 NORMAL"

            action = (
                "استمرار المراقبة"
            )





        warnings[area] = {


            "level":

                level,


            "score":

                score,


            "reasons":

                reasons,


            "action":

                action

        }





    return warnings
