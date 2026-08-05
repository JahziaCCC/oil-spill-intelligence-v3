import os
import json
import asyncio
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

AIS_CACHE_FILE = "data/ais_cache.json"


# اختبار استقبال AIS من قناة السويس ومحيطها
BBOXES = [
    [
        [27.0, 29.0],
        [33.0, 35.0]
    ]
]



def save_cache(vessels):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        AIS_CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            vessels,
            f,
            ensure_ascii=False,
            indent=2
        )



def load_cache():

    if not os.path.exists(
        AIS_CACHE_FILE
    ):
        return []

    try:

        with open(
            AIS_CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []





async def collect_ais():

    print()

    print("=" * 60)

    print("تشغيل AIS Collector")

    print("=" * 60)



    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )


    if not api_key:

        print(
            "❌ AISSTREAM_API_KEY غير موجود"
        )

        return []



    print(
        "AIS KEY EXISTS: True LENGTH:",
        len(api_key)
    )



    vessels = []



    try:


        async with websockets.connect(
            AISSTREAM_URL,
            ping_interval=20,
            ping_timeout=20
        ) as websocket:



            print(
                "✅ AIS Connected"
            )



            subscription = {

                "APIKey": api_key,

                "BoundingBoxes": BBOXES,

                "FilterMessageTypes": [
                    "PositionReport"
                ]

            }



            await websocket.send(
                json.dumps(subscription)
            )



            print(
                "✅ Subscription sent"
            )



            print(
                "⏳ Collecting AIS data..."
            )



            start_time = (
                asyncio.get_event_loop()
                .time()
            )



            while (

                asyncio.get_event_loop().time()
                -
                start_time

                <
                120

            ):


                try:


                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=15
                    )



                    data = json.loads(
                        message
                    )



                    # معرفة نوع الرسالة للتشخيص

                    message_type = (
                        data
                        .get(
                            "MessageType"
                        )
                    )


                    if message_type:

                        print(
                            "📡 AIS MESSAGE:",
                            message_type
                        )



                    position = (

                        data
                        .get(
                            "Message",
                            {}
                        )
                        .get(
                            "PositionReport"
                        )

                    )



                    metadata = (

                        data
                        .get(
                            "MetaData",
                            {}
                        )

                    )



                    if position:



                        vessel = {


                            "mmsi":

                            metadata.get(
                                "MMSI"
                            ),



                            "name":

                            metadata.get(
                                "ShipName",
                                ""
                            ).strip(),



                            "lat":

                            position.get(
                                "Latitude"
                            ),



                            "lon":

                            position.get(
                                "Longitude"
                            ),



                            "speed":

                            position.get(
                                "Sog"
                            ),



                            "heading":

                            position.get(
                                "TrueHeading"
                            ),



                            "timestamp":

                            metadata.get(
                                "time_utc"
                            )

                        }



                        vessels.append(
                            vessel
                        )



                        print(
                            "🚢",
                            vessel["name"],
                            "|",
                            vessel["lat"],
                            vessel["lon"]
                        )



                except asyncio.TimeoutError:

                    continue




    except Exception as e:


        print(
            "AIS ERROR:",
            e
        )





    # إذا لم تصل بيانات نستخدم آخر Cache

    if len(vessels) == 0:


        print()

        print(
            "⚠️ لم يتم استقبال سفن جديدة"
        )


        cache = load_cache()



        if len(cache) > 0:


            print(
                "♻️ استخدام آخر بيانات AIS محفوظة"
            )


            vessels = cache



        else:


            print(
                "❌ لا يوجد AIS Cache"
            )



    else:


        save_cache(
            vessels
        )



    print()

    print("=" * 50)

    print("AIS SUMMARY")

    print("=" * 50)



    print(
        "AIS Vessels Received:",
        len(vessels)
    )



    if len(vessels) > 0:

        print(
            "AIS DATA STATUS: ONLINE"
        )


        print(
            "AIS QUALITY: GOOD"
        )


    else:


        print(
            "AIS DATA STATUS: OFFLINE"
        )


        print(
            "AIS QUALITY: LOW"
        )



    print("=" * 50)



    return vessels
