import asyncio
from datetime import datetime, timezone

from ais.collector import collect_ais

from intelligence.maritime_engine import analyze_maritime

from intelligence.trend_engine import analyze_trend

from intelligence.history_db import (
    create_database,
    save_report
)



def header(title):

    print()

    print("=" * 60)

    print(title)

    print("=" * 60)





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
# AIS DATA
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
# RISK ANALYSIS
# =========================



header(
    "تشغيل محرك تحليل المخاطر البحرية"
)



risk_report = analyze_maritime(
    vessels
)



print(
    "تم الانتهاء من تحليل المخاطر."
)




# =========================
# HISTORICAL DATABASE
# =========================



create_database()



save_report(
    risk_report
)



print(
    "✅ Historical Risk Database Updated"
)




# =========================
# TREND ANALYSIS
# =========================



trend_report = analyze_trend(
    risk_report
)




# =========================
# MARITIME REPORT
# =========================



header(
    "تقرير المخاطر البحرية"
)



highest_area = None

highest_score = -1

total_ships = 0




for area,data in risk_report.items():


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



    print(
        "اتجاه المخاطر:",
        trend_report.get(
            area,
            {}
        ).get(
            "trend",
            "غير متوفر"
        )
    )



    print(
        "تغير الدرجة:",
        trend_report.get(
            area,
            {}
        ).get(
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




for area,data in risk_report.items():


    score = data.get(
        "risk_score",
        0
    )


    print()

    print(
        "📍",
        area
    )



    if score >= 70:

        alert = "🔴 RED ALERT"

        action = (
            "رفع مستوى الجاهزية التشغيلية الفورية"
        )


    elif score >= 30:

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



    if score >= 30:


        print(
            "الأسباب:"
        )


        if data.get(
            "ships",
            0
        ) >= 20:

            print(
                "- كثافة سفن عالية"
            )


        if data.get(
            "tankers",
            0
        ) > 0:

            print(
                "- وجود ناقلات نفط"
            )


        if data.get(
            "strategic",
            0
        ) > 0:

            print(
                "- وجود سفن استراتيجية"
            )



    print(
        "الإجراء:",
        action
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



if highest_score >= 70:

    status = "🔴 RED ALERT"


elif highest_score >= 30:

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
