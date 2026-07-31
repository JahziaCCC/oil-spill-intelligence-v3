import asyncio

from ais.collector import collect_ais
from ais.tracker import update_track


def print_header():

    print("=" * 50)
    print("Oil Spill Intelligence V3")
    print("AIS INTELLIGENCE ENGINE")
    print("=" * 50)
    print()



def print_summary(vessels, tracks):

    print()
    print("=" * 50)
    print("ملخص نظام AIS")
    print("=" * 50)

    print("عدد السفن المرصودة:", len(vessels))

    print("تم تحديث سجل المسارات")

    print("عدد السفن المتتبعة:", len(tracks))

    print("=" * 50)



def generate_report(vessels):

    print()
    print("=" * 50)
    print("تقرير المخاطر البحرية على المضائق")
    print("=" * 50)


    chokepoints = {

        "مضيق هرمز": {
            "lat": 26.5,
            "lon": 56.5
        },

        "باب المندب": {
            "lat": 12.5,
            "lon": 43.5
        },

        "قناة السويس": {
            "lat": 30.5,
            "lon": 32.3
        }

    }


    for name, point in chokepoints.items():

        count = 0


        for vessel in vessels:

            lat = vessel.get("lat")
            lon = vessel.get("lon")


            if not lat or not lon:
                continue


            distance = (
                abs(lat - point["lat"])
                +
                abs(lon - point["lon"])
            )


            if distance < 5:

                count += 1



        risk = "منخفض"

        score = 0


        if count > 20:

            risk = "متوسط"
            score = 40


        elif count > 50:

            risk = "مرتفع"
            score = 70



        print()
        print(name)

        print("عدد السفن:", count)

        print("درجة المخاطر:", score)

        print("مستوى المخاطر:", risk)



    print()
    print("=" * 50)
    print("اكتمل محرك الذكاء البحري")
    print("=" * 50)



async def main():

    print_header()


    vessels = await collect_ais()


    tracks = update_track(vessels)


    print_summary(
        vessels,
        tracks
    )


    generate_report(
        vessels
    )



if __name__ == "__main__":

    asyncio.run(main())
