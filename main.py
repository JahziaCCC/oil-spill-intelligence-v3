import asyncio
from datetime import datetime, timezone

from ais.collector import collect_ais
from intelligence.maritime_engine import analyze_maritime


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


print("وقت التشغيل :", time_now)



# =========================
# AIS DATA
# =========================


vessels = asyncio.run(
    collect_ais()
)



header("ملخص نظام AIS")


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
# ANALYSIS
# =========================


risk_report = analyze_maritime(
    vessels
)



header(
    "تقرير المخاطر البحرية"
)



highest_area = None
highest_score = -1

total_ships = 0



for area,data in risk_report.items():


    print()

    print("📍", area)

    print("-"*40)



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
# THREAT ANALYSIS
# =========================


header(
    "تقرير التهديدات البحرية"
)


for area,data in risk_report.items():

    threats=[]


    if data.get("strategic",0)>0:

        threats.append(
            "سفن استراتيجية"
        )


    if data.get("stopped",0)>=10:

        threats.append(
            "ازدحام أو توقف ملاحي"
        )


    if data.get("tankers",0)>0:

        threats.append(
            "وجود ناقلات نفط"
        )



    print()

    print("📍",area)


    if threats:

        print(
            "مستوى التأثير: HIGH"
        )

        for t in threats:

            print(
                "-",
                t
            )

    else:

        print(
            "مستوى التأثير: LOW"
        )

        print(
            "- لا توجد تهديدات مكتشفة"
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



if highest_score >=70:

    status="🔴 حرج"

elif highest_score >=50:

    status="🟠 مرتفع"

elif highest_score >=25:

    status="🟡 متوسط"

else:

    status="🟢 منخفض"



print(
    "الحالة العامة:",
    status
)


print("=" * 60)

print(
    "اكتمل تشغيل محرك الذكاء البحري"
)
