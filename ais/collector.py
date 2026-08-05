import os
import json
import asyncio
import websockets

from ais.cache import (
    save_ais_cache,
    load_ais_cache
)


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"


BBOXES = [

    [
        [22.0, 50.0],
        [30.0, 62.0]
    ],

    [
        [8.0, 38.0],
        [16.0, 47.0]
    ],

    [
        [27.0, 29.0],
        [33.0, 35.0]
    ]

]



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
            "❌ Missing AISSTREAM_API_KEY"
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

                "APIKey":
                api_key,


                "BoundingBoxes":
                BBOXES,


                "FilterMessageTypes":
                [
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



            start = asyncio.get_event_loop().time()



            while (

                asyncio.get_event_loop().time()
                -
                start

                <
                60

            ):


                try:


                    message = await asyncio.wait_for(

                        websocket.recv(),

                        timeout=8

                    )


                    data = json.loads(
                        message
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



                    metadata = data.get(
                        "MetaData",
                        {}
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


                    print(
                        "⏳ Waiting AIS message..."
                    )

                    continue





    except Exception as e:


        print(
            "AIS ERROR:",
            e
        )





    # ==========================
    # البيانات الجديدة
    # ==========================


    if len(vessels) > 0:



        save_ais_cache(
            vessels
        )



        print(
            "🟢 AIS DATA STATUS: ONLINE"
        )



        print(
            "AIS QUALITY: HIGH"
        )



    else:



        print()
        print(
            "⚠️ لم يتم استقبال سفن جديدة"
        )



        vessels = load_ais_cache()



        if len(vessels) > 0:



            print(
                "🟡 AIS DATA STATUS: CACHE"
            )


            print(
                "AIS QUALITY: MEDIUM"
            )



        else:


            print(

            )


            print(
                "🔴 AIS DATA STATUS: OFFLINE"
            )


            print(
                "AIS QUALITY: LOW"
            )





    print()

    print("=" * 50)
    print("AIS SUMMARY")
    print("=" * 50)


    print(
        "AIS Vessels Received:",
        len(vessels)
    )

    print("=" * 50)



    return vessels
