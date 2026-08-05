import os
import json
import asyncio
import websockets

from datetime import datetime, timezone


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

AIS_CACHE_FILE = "data/ais_cache.json"


# مناطق المراقبة
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



def save_cache(vessels):

    os.makedirs(
        "data",
        exist_ok=True
    )


    data = {

        "updated":

            datetime.now(
                timezone.utc
            ).strftime(
                "%Y-%m-%d %H:%M UTC"
            ),

        "count":

            len(vessels),

        "vessels":

            vessels
    }


    with open(
        AIS_CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


    print(
        "✅ AIS CACHE SAVED"
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


            data = json.load(f)


        vessels = data.get(
            "vessels",
            []
        )


        return vessels


    except Exception:

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



    attempts = 3



    for attempt in range(
        1,
        attempts + 1
    ):


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


                        print(
                            "⏳ Waiting AIS message..."
                        )


                        continue




                break




        except Exception as e:


            print(
                "AIS CONNECTION ERROR:",
                e
            )


            if attempt < attempts:


                print(
                    "🔄 إعادة المحاولة..."
                )


                await asyncio.sleep(
                    5
                )





    # ==========================
    # Data Decision
    # ==========================


    if vessels:


        save_cache(
            vessels
        )


        status = "REALTIME"

        quality = "HIGH"



    else:


        cached = load_cache()



        if cached:


            vessels = cached


            print(
                "♻️ استخدام آخر AIS Cache"
            )


            status = "CACHE"

            quality = "MEDIUM"



        else:


            os.makedirs(
                "data",
                exist_ok=True
            )


            save_cache(
                []
            )


            print(
                "⚠️ AIS Cache موجود ولكن بدون بيانات"
            )


            status = "OFFLINE"

            quality = "LOW"




    print()

    print("=" * 50)
    print("AIS SUMMARY")
    print("=" * 50)



    print(
        "AIS Vessels Received:",
        len(vessels)
    )


    print(
        "AIS DATA STATUS:",
        status
    )


    print(
        "AIS QUALITY:",
        quality
    )


    print("=" * 50)



    return vessels
