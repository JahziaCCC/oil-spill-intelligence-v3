import asyncio


from ais.collector import collect_ais


from intelligence.maritime_engine import analyze_maritime


from intelligence.vessel_tracker import update_vessel_tracks





print("=" * 50)
print("Oil Spill Intelligence V3")
print("AIS INTELLIGENCE ENGINE")
print("=" * 50)





async def run():


    print()

    print("AIS Collector Starting...")


    vessels = await collect_ais()



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
    print("ملخص نظام AIS")
    print("=" * 50)



    print(
        "عدد السفن المرصودة:",
        len(vessels)
    )



    tracked = update_vessel_tracks(
        vessels
    )



    print(
        "تم تحديث سجل المسارات"
    )


    print(
        "عدد السفن المتتبعة:",
        len(tracked)
    )



    print("=" * 50)






    print()

    print("=" * 50)
    print("تقرير المخاطر البحرية على المضائق")
    print("=" * 50)



    report = analyze_maritime()



    for zone, data in report.items():

        print()

        print(zone)


        print(
            "عدد السفن:",
            data.get(
                "عدد السفن",
                data.get("vessels",0)
            )
        )


        print(
            "ناقلات محتملة:",
            data.get(
                "ناقلات محتملة",
                data.get("tankers",0)
            )
        )


        if "سفن متحركة" in data:

            print(
                "سفن متحركة:",
                data["سفن متحركة"]
            )


        if "سفن متوقفة" in data:

            print(
                "سفن متوقفة:",
                data["سفن متوقفة"]
            )



        if "مؤشر الحركة" in data:

            print(
                "مؤشر الحركة:",
                data["مؤشر الحركة"]
            )


        print(
            "درجة المخاطر:",
            data.get(
                "درجة المخاطر",
                data.get("risk_score",0)
            )
        )



        print(
            "مستوى المخاطر:",
            data.get(
                "مستوى المخاطر",
                data.get("risk_level","")
            )
        )



        if "التوصية" in data:

            print(
                "التوصية:",
                data["التوصية"]
            )




    print()

    print("=" * 50)
    print("اكتمل محرك الذكاء البحري")
    print("=" * 50)






if __name__ == "__main__":

    asyncio.run(
        run()
    )
