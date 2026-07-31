import asyncio
from datetime import datetime, timezone

from ais.collector import collect_ais
from intelligence.maritime_engine import analyze_maritime
from intelligence.trend_engine import calculate_trend



print("=" * 60)
print("Oil Spill Intelligence V3")
print("Strategic Maritime Intelligence Engine")
print("=" * 60)



time_now = datetime.now(
    timezone.utc
).strftime(
    "%Y-%m-%d %H:%M UTC"
)


print(
    "وقت التشغيل :",
    time_now
)

print()



# ==========================
# AIS COLLECTION
# ==========================


vessels = asyncio.run(
    collect_ais()
)



print()

print("=" * 60)
print("ملخص نظام AIS")
print("=" * 60)


print(
    "عدد السفن المرصودة:",
    len(vessels)
)


print(
    "تم تحديث سجل المسارات"
)


print(
    "عدد السفن المتتبعة:",
    len(vessels)
)


print("=" * 60)



# ==========================
# RISK ANALYSIS
# ==========================


risk_report = analyze_maritime(
    vessels
)



print()

print("=" * 60)
print("تقرير المخاطر البحرية")
print("=" * 60)



highest = None
highest_score = -1

total_inside = 0



for name, data in risk_report.items():


    print()

    print("📍", name)

    print("-" * 40)



    ships = data.get(
        "ships",
        0
    )


    total_inside += ships



    score = data.get(
        "risk_score",
        0
    )



    # تحليل اتجاه المخاطر

    trend_data = calculate_trend(
        name,
        score
    )



    if score > highest_score:

        highest_score = score
        highest = name



    print(
        "الأهمية الاستراتيجية :",
        data.get(
            "impact",
            "غير محدد"
        )
    )


    print(
        "عدد السفن           :",
        ships
    )


    print(
        "ناقلات النفط        :",
        data.get(
            "tankers",
            0
        )
    )


    print(
        "سفن استراتيجية      :",
        data.get(
            "strategic",
            0
        )
    )


    print(
        "السفن المتحركة      :",
        data.get(
            "moving",
            0
        )
    )


    print(
        "السفن المتوقفة      :",
        data.get(
            "stopped",
            0
        )
    )


    print(
        "كثافة الحركة        :",
        data.get(
            "movement_density",
            0
        ),
        "%"
    )


    print(
        "نسبة الناقلات       :",
        data.get(
            "tanker_ratio",
            0
        ),
        "%"
    )


    print(
        "درجة المخاطر        :",
        score
    )


    print(
        "اتجاه المخاطر       :",
        trend_data.get(
            "trend"
        )
    )


    print(
        "تغير الدرجة         :",
        trend_data.get(
            "change"
        )
    )


    print(
        "مستوى المخاطر       :",
        data.get(
            "risk_level",
            ""
        )
    )


    print(
        "الجاهزية            :",
        data.get(
            "readiness",
            ""
        )
    )


    print(
        "التوصية             :",
        data.get(
            "recommendation",
            ""
        )
    )





# ==========================
# EXECUTIVE SUMMARY
# ==========================


print()

print("=" * 60)
print("الملخص التنفيذي")
print("=" * 60)



print(
    "إجمالي السفن داخل المضائق :",
    total_inside
)



print(
    "أعلى منطقة خطورة :",
    highest
)



print(
    "درجة الخطورة :",
    highest_score
)



if highest_score >= 75:

    status = "🔴 حرج"


elif highest_score >= 50:

    status = "🟠 مرتفع"


elif highest_score >= 25:

    status = "🟡 متوسط"


else:

    status = "🟢 منخفض"



print(
    "الحالة العامة :",
    status
)



print("=" * 60)


print(
    "اكتمل تشغيل محرك الذكاء البحري"
)
