from intelligence.risk_engine import calculate_risk
from datetime import datetime, timezone


def analyze_maritime(vessels):

    report_time = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )

    print()
    print("=" * 60)
    print("تشغيل محرك تحليل المخاطر البحرية")
    print("=" * 60)

    print("وقت التحليل:", report_time)
    print("السفن الداخلة للتحليل:", len(vessels))


    # تشغيل محرك المخاطر
    report = calculate_risk(vessels)


    # إضافة مؤشرات استخباراتية
    for area, data in report.items():

        ships = data.get("ships",0)
        tankers = data.get("tankers",0)
        moving = data.get("moving",0)
        stopped = data.get("stopped",0)


        density = 0

        if ships > 0:
            density = round(
                (moving / ships) * 100,
                1
            )


        tanker_ratio = 0

        if ships > 0:
            tanker_ratio = round(
                (tankers / ships) * 100,
                1
            )


        data["traffic_density"] = density

        data["tanker_ratio"] = tanker_ratio


        # مستوى الجاهزية

        score = data.get(
            "risk_score",
            0
        )


        if score >= 75:
            readiness = "حرج"

        elif score >=50:
            readiness = "مرتفع"

        elif score >=25:
            readiness = "متوسط"

        else:
            readiness = "منخفض"


        data["readiness"] = readiness



    print("تم الانتهاء من تحليل المخاطر.")

    return report
