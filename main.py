import asyncio
from datetime import datetime, timezone

from ais.collector import collect_ais
from intelligence.maritime_engine import analyze_maritime
from intelligence.trend_engine import analyze_trend
from intelligence.history_db import create_database, save_report


def header(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def get_alert(score):

    if score >= 70:
        return (
            "🔴 RED ALERT",
            "رفع مستوى الجاهزية التشغيلية الفورية"
        )

    elif score >= 30:
        return (
            "🟡 YELLOW ALERT",
            "مراقبة مستمرة"
        )

    else:
        return (
            "🟢 NORMAL",
            "استمرار المراقبة"
        )


# ==================================================
# START
# ==================================================

header(
    "Oil Spill Intelligence V3\nStrategic Maritime Intelligence Engine"
)


time_now = datetime.now(
    timezone.utc
).strftime("%Y-%m-%d %H:%M UTC")


print("وقت التشغيل :", time_now)



# ==================================================
# AIS
# ==================================================

header("تشغيل AIS Collector")


try:

    vessels = asyncio.run(
        collect_ais()
    )


except Exception as e:

    print("❌ AIS ERROR:", e)

    vessels = []



header("ملخص نظام AIS")


print(
    "عدد السفن المرصودة:",
    len(vessels)
)

print(
    "حالة النظام:",
    "ONLINE" if vessels else "OFFLINE"
)

print(
    "مصدر البيانات:",
    "AIS REAL TIME"
)



# ==================================================
# RISK ENGINE
# ==================================================

header(
    "تشغيل محرك تحليل المخاطر البحرية"
)


try:

    risk_report = analyze_maritime(
        vessels
    )

    print(
        "✅ تم الانتهاء من تحليل المخاطر"
    )


except Exception as e:

    print(
        "❌ Risk Engine Error:",
        e
    )

    risk_report = {}



# ==================================================
# HISTORY
# ==================================================

try:

    create_database()

    save_report(
        risk_report
    )

    print(
        "✅ Historical Risk Database Updated"
    )


except Exception as e:

    print(
        "⚠️ History Database Error:",
        e
    )



# ==================================================
# TREND
# ==================================================

try:

    trend_report = analyze_trend(
        risk_report
    )

except:

    trend_report = {}



# ==================================================
# REPORT
# ==================================================

header(
    "تقرير المخاطر البحرية"
)


highest_area = None
highest_score = 0
total_ships = 0



for area, data in risk_report.items():


    score = data.get(
        "risk_score",
        0
    )


    ships = data.get(
        "ships",
        0
    )


    total_ships += ships


    if score > highest_score:

        highest_score = score
        highest_area = area



    print()
    print("📍", area)
    print("-" * 40)


    print(
        "الأهمية:",
        data.get(
            "strategic_importance"
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


    alert, action = get_alert(
        score
    )


    print()
    print(
        "📍",
        area
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

        if data.get("ships",0) >= 20:
            print(
                "- كثافة سفن عالية"
            )

        if data.get("tankers",0):
            print(
                "- وجود ناقلات نفط"
            )

        if data.get("strategic",0):
            print(
                "- وجود سفن استراتيجية"
            )


    print(
        "الإجراء:",
        action
    )



# ==================================================
# EXECUTIVE
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



final_alert, _ = get_alert(
    highest_score
)


print(
    "الحالة العامة:",
    final_alert
)


print("=" * 60)

print(
    "اكتمل تشغيل محرك الذكاء البحري"
)
