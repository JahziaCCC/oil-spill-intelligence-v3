import asyncio

from ais.collector import collect_ais
from intelligence.maritime_engine import analyze_maritime


print("=" * 50)
print("Oil Spill Intelligence V3")
print("AIS INTELLIGENCE ENGINE")
print("=" * 50)


async def main():

    # تشغيل AIS Collector
    vessels = await collect_ais(
        duration=120
    )


    print()

    print("=" * 50)
    print("AIS SUMMARY")
    print("=" * 50)

    print(
        "AIS Vessels Received:",
        len(vessels)
    )

    print(
        "AIS CACHE UPDATED"
    )

    print("=" * 50)


    print()

    print("=" * 50)
    print("MARITIME RISK REPORT")
    print("=" * 50)


    report = analyze_maritime()


    for area, data in report.items():

        print()

        print(area)

        print(
            "Vessels:",
            data["vessels"]
        )

        print(
            "Risk Score:",
            data["risk_score"]
        )

        print(
            "Risk Level:",
            data["risk_level"]
        )


    print()
    print("=" * 50)
    print("INTELLIGENCE ENGINE COMPLETED")
    print("=" * 50)



if __name__ == "__main__":

    asyncio.run(main())
