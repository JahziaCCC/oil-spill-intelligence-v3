import asyncio
from datetime import datetime, timezone

from ais.collector import collect_ais
from intelligence.maritime_engine import analyze_maritime
from intelligence.trend_engine import analyze_trend


def header(title):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)



# =========================
# SYSTEM HEADER
# =========================

header(
    "Oil Spill Intelligence V3\nStrategic Maritime Intelligence Engine"
)


time_now = datetime.now(
    timezone.utc
).strftime(
    "%Y-%m-%d %H:%M UTC"
)


print(
    "وقت التشغيل :",
    time_now
)



# =========================
# AIS COLLECTION
# =========================


vessels = asyncio.run(
    collect_ais()
)



header(
    "ملخص نظام AIS"
)


print(
    "عدد السفن المرصودة:",
    len(vessels)
)


print(
    "حالة النظام:",
    "ONLINE"
)


print(
    "مصدر البيانات:",
    "AIS REAL TIME"
)



# =========================
# MARITIME ANALYSIS
# =========================


risk_report = analyze_maritime(
    vessels
)



trend_report = analyze_trend(
    risk_report
)



header(
    "تقرير المخاطر البحرية"
)



highest_area = None
highest_score = -1

total_ships = 0



for area, data in risk_report.items():


    print()

    print(
        "📍",
        area
    )

    print(
        "-" * 40
    )



    ships = data.get(
        "ships",
        0
    )


    score = data.get(
        "risk_score",
        0
    )


    total_ships += ships



    if score > highest_score:

        highest_score = score
        highest_area = area




    print(
        "الأهمية الاستراتيجية :",
        data.get(
            "strategic_importance",
            "غير محدد"
        )
    )


    print(
        "عدد السفن:",
        ships
    )


    print(
        "السفن القريبة:",
        data.get(
            "nearby",
            0
        )
    )


    print(
        "ناقلات النفط:",
        data.get(
            "tankers",
            0
        )
    )


    print(
        "السفن الاستراتيجية:",
        data.get(
            "strategic",
            0
        )
    )


    print(
        "السفن المتحركة:",
        data.get(
            "moving",
            0
        )
    )


    print(
        "السفن المتوقفة:",
        data.get(
            "stopped",
            0
        )
    )


    print(
        "درجة المخاطر:",
        score
    )



    trend = trend_report.get(
        area,
        {}
    )


    print(
        "اتجاه المخاطر:",
        trend.get(
            "trend",
            "⚪ مستقر"
        )
    )


    print(
        "تغير الدرجة:",
        trend.get(
            "difference",
            0
        )
    )



    print(
        "مستوى المخاطر:",
        data.get(
            "risk_level"
        )
    )


    print(
        "الجاهزية:",
        data.get(
            "readiness"
        )
    )


    print(
        "التوصية:",
        data.get(
            "recommendation"
        )
    )





# =========================
# EARLY WARNING SYSTEM
# =========================


header(
    "نظام الإنذار المبكر البحري"
)



for area, data in risk_report.items():


    score = data.get(
        "risk_score",
        0
    )


    print()

    print(
        "📍",
        area
    )



    if score >= 80:

        alert = "🔴 RED ALERT"

        action = (
            "رفع مستوى الجاهزية التشغيلية الفورية"
        )


    elif score >= 50:

        alert = "🟠 ORANGE ALERT"

        action = (
            "زيادة المتابعة والتحليل"
        )


    elif score >= 25:

        alert = "🟡 YELLOW ALERT"

        action = (
            "مراقبة مستمرة"
        )


    else:

        alert = "🟢 NORMAL"

        action = (
            "استمرار المراقبة"
        )



    print(
        "مستوى الإنذار:",
        alert
    )


    print(
        "درجة الخطر:",
        score
    )



    reasons = data.get(
        "alert_reasons",
        []
    )


    if reasons:

        print(
            "الأسباب:"
        )

        for reason in reasons:

            print(
                "-",
                reason
            )


    print(
        "الإجراء:",
        action
    )






# =========================
# THREAT ANALYSIS
# =========================


header(
    "تقرير التهديدات البحرية"
)



for area, data in risk_report.items():


    score = data.get(
        "risk_score",
        0
    )


    print()

    print(
        "📍",
        area
    )



    if score >= 80:

        impact = "HIGH"


    elif score >= 50:

        impact = "MEDIUM"


    else:

        impact = "LOW"



    print(
        "مستوى التأثير:",
        impact
    )



    reasons = data.get(
        "alert_reasons",
        []
    )



    if reasons:

        for reason in reasons:

            print(
                "-",
                reason
            )

    else:

        print(
            "- لا توجد تهديدات مكتشفة"
        )



    if score >= 50:

        print(
            "التوصية: رفع مستوى المتابعة"
        )





# =========================
# EXECUTIVE SUMMARY
# =========================


header(
    "الملخص التنفيذي"
)



print(
    "إجمالي السفن داخل المضائق:",
    total_ships
)



print(
    "أعلى منطقة خطورة:",
    highest_area
)



print(
    "درجة الخطورة:",
    highest_score
)



if highest_score >= 80:

    status = "🔴 RED ALERT"


elif highest_score >= 50:

    status = "🟠 ORANGE ALERT"


elif highest_score >= 25:

    status = "🟡 YELLOW ALERT"


else:

    status = "🟢 NORMAL"



print(
    "الحالة العامة:",
    status
)



print(
    "=" * 60
)


print(
    "اكتمل تشغيل محرك الذكاء البحري"
)
