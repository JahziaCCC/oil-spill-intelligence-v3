import asyncio

from ais.collector import collect_ais
from intelligence.maritime_engine import calculate_risk


print("=" * 50)
print("Oil Spill Intelligence V3")
print("AIS INTELLIGENCE ENGINE")
print("=" * 50)


async def main():

    # ===============================
    # AIS COLLECTION
    # ===============================

    vessels = await collect_ais()


    print()
    print("=" * 50)
    print("ملخص نظام AIS")
    print("=" * 50)

    print("عدد السفن المرصودة:", len(vessels))
    print("تم تحديث سجل المسارات")
    print("عدد السفن المتتبعة:", len(vessels))

    print("=" * 50)



    # ===============================
    # MARITIME RISK ENGINE
    # ===============================

    risk_report = calculate_risk(vessels)


    print()
    print("=" * 50)
    print("تقرير المخاطر البحرية على المضائق")
    print("=" * 50)


    for area, data in risk_report.items():

        print()
        print(area)

        print(
            "عدد السفن:",
            data["ships"]
        )

        print(
            "ناقلات محتملة:",
            data["tankers"]
        )

        print(
            "درجة المخاطر:",
            data["risk_score"]
        )

        print(
            "مستوى المخاطر:",
            data["risk_level"]
        )


    print()
    print("=" * 50)
    print("اكتمل محرك الذكاء البحري")
    print("=" * 50)



if __name__ == "__main__":

    asyncio.run(main())
