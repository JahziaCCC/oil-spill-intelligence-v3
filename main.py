import asyncio

from ais.collector import collect_ais
from ais.tracker import update_track
from intelligence.maritime_risk import calculate_risk


def print_header():

    print("=" * 50)
    print("Oil Spill Intelligence V3")
    print("AIS INTELLIGENCE ENGINE")
    print("=" * 50)
    print()



def print_ais_summary(vessels, tracks):

    print()
    print("=" * 50)
    print("ملخص نظام AIS")
    print("=" * 50)

    print("عدد السفن المرصودة:", len(vessels))
    print("تم تحديث سجل المسارات")
    print("عدد السفن المتتبعة:", len(tracks))

    print("=" * 50)



def print_maritime_report(report):

    print()
    print("=" * 50)
    print("تقرير المخاطر البحرية على المضائق")
    print("=" * 50)


    for area, data in report.items():

        print()
        print(area)

        print("عدد السفن:", data["ships"])
        print("ناقلات محتملة:", data["tankers"])
        print("درجة المخاطر:", data["risk_score"])
        print("مستوى المخاطر:", data["risk_level"])


    print()
    print("=" * 50)
    print("اكتمل محرك الذكاء البحري")
    print("=" * 50)



async def main():

    print_header()


    # جمع بيانات السفن من AIS

    vessels = await collect_ais()


    # تحديث مسارات السفن

    tracks = update_track(vessels)


    # حساب مخاطر المضائق

    risk_report = calculate_risk(vessels)



    print_ais_summary(
        vessels,
        tracks
    )


    print_maritime_report(
        risk_report
    )



if __name__ == "__main__":

    asyncio.run(main())
