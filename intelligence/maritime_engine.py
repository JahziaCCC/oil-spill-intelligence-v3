from intelligence.risk_engine import calculate_risk
from datetime import datetime, timezone



def analyze_maritime(vessels):

    """
    Strategic Maritime Risk Analysis Engine

    Input:
        AIS vessels list

    Output:
        Maritime risk intelligence report
    """

    report_time = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M UTC"
    )


    # تشغيل محرك المخاطر الأساسي

    report = calculate_risk(
        vessels
    )


    # إضافة طبقة التحليل الاستخباراتي

    for area, data in report.items():


        ships = data.get(
            "ships",
            0
        )

        tankers = data.get(
            "tankers",
            0
        )

        strategic = data.get(
            "strategic",
            0
        )

        moving = data.get(
            "moving",
            0
        )

        stopped = data.get(
            "stopped",
            0
        )


        # =========================
        # Traffic Indicators
        # =========================


        traffic_density = 0

        if ships > 0:

            traffic_density = round(
                (moving / ships) * 100,
                1
            )



        tanker_ratio = 0

        if ships > 0:

            tanker_ratio = round(
                (tankers / ships) * 100,
                1
            )



        stopped_ratio = 0

        if ships > 0:

            stopped_ratio = round(
                (stopped / ships) * 100,
                1
            )



        data["traffic_density"] = traffic_density

        data["tanker_ratio"] = tanker_ratio

        data["stopped_ratio"] = stopped_ratio



        # =========================
        # Intelligence Score
        # =========================


        score = data.get(
            "risk_score",
            0
        )


        # إضافة عامل ازدحام

        if ships >= 20:

            score += 10



        # إضافة عامل ناقلات النفط

        if tankers >= 2:

            score += 10



        # إضافة عامل السفن الاستراتيجية

        if strategic >= 2:

            score += 10



        # منع تجاوز 100

        if score > 100:

            score = 100



        data["risk_score"] = score



        # =========================
        # Readiness Level
        # =========================


        if score >= 80:

            readiness = "حرج"


        elif score >= 60:

            readiness = "مرتفع"


        elif score >= 30:

            readiness = "متوسط"


        else:

            readiness = "منخفض"



        data["readiness"] = readiness



        # =========================
        # Recommendation
        # =========================


        if score >= 80:

            recommendation = (
                "رفع مستوى الجاهزية التشغيلية "
                "وتفعيل المتابعة المستمرة"
            )


        elif score >= 60:

            recommendation = (
                "زيادة المتابعة والتحليل"
            )


        elif score >= 30:

            recommendation = (
                "مراقبة مستمرة"
            )


        else:

            recommendation = (
                "استمرار المراقبة"
            )



        data["recommendation"] = recommendation



        # Metadata للـ Dashboard

        data["analysis_time"] = report_time

        data["intelligence_status"] = (
            "ACTIVE"
        )



    return report
