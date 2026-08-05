import asyncio
from datetime import datetime, timezone


from ais.collector import collect_ais

from intelligence.maritime_engine import analyze_maritime

from intelligence.trend_engine import analyze_trend

from intelligence.history_db import (
    create_database,
    save_report
)

from intelligence.events_engine import (
    detect_events
)



def header(title):

    print()

    print("=" * 60)

    print(title)

    print("=" * 60)



# ==================================================
# SYSTEM START
# ==================================================

header(
    "Oil Spill Intelligence V3\n"
    "Strategic Maritime Intelligence Engine"
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



# ==================================================
# AIS COLLECTION
# ==================================================

header(
    "تشغيل AIS Collector"
)


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


if len(vessels) > 0:

    print(
        "حالة النظام:",
        "ONLINE"
    )

else:

    print(
        "حالة النظام:",
        "OFFLINE"
    )


print(
    "مصدر البيانات:",
    "AIS REAL TIME"
)




# ==================================================
# MARITIME RISK ENGINE
# ==================================================

header(
    "تشغيل محرك تحليل المخاطر البحرية"
)


risk_report = analyze_maritime(
    vessels
)


print(
    "✅ تم الانتهاء من تحليل المخاطر"
)




# ==================================================
# DATABASE
# ==================================================

create_database()


save_report(
    risk_report
)


print(
    "✅ Historical Risk Database Updated"
)




# ==================================================
# TREND ENGINE
# ==================================================

trend_report = analyze_trend(
    risk_report
)




# ==================================================
# EVENTS ENGINE
# ==================================================

events = detect_events(
    risk_report
)




# ==================================================
# RISK REPORT
# ==================================================

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
        "الأهمية:",
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
        "الاتجاه:",
        trend_report.get(
            area,
            {}
        ).get(
            "trend",
            "مستقر"
        )
    )


    print(
        "مستوى الخطر:",
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




# ==================================================
# EARLY WARNING
# ==================================================

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


    print(
        "الإجراء:",
        action
    )




# ==================================================
# MARITIME EVENTS
# ==================================================

header(
    "الأحداث البحرية المكتشفة"
)



if events:


    for event in events:

        print()

        print(
            "📌 المنطقة:",
            event["area"]
        )


        print(
            "الحدث:",
            event["type"]
        )


        print(
            "المستوى:",
            event["severity"]
        )


        print(
            "التفاصيل:",
            event["message"]
        )


        print(
            "الوقت:",
            event["time"]
        )


else:


    print(
        "لا توجد أحداث بحرية غير طبيعية"
    )





# ==================================================
# EXECUTIVE SUMMARY
# ==================================================

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
