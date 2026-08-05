import os
import json
import asyncio
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

AIS_CACHE_FILE = "data/ais_cache.json"


print("COLLECTOR VERSION: V5 ACTIVE")


# مناطق استراتيجية دقيقة
# صيغة AISStream:
# [ [lat_min, lon_min], [lat_max, lon_max] ]

BBOXES = [

    # Strait of Hormuz
    [
        [24.0, 54.0],
        [28.5, 60.5]
    ],


    # Bab Al Mandab
    [
        [11.0, 42.0],
        [14.5, 45.5]
    ],


    # Suez Canal
    [
        [29.0, 31.0],
        [32.5, 33.5]
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
            "❌ AIS KEY NOT FOUND"
        )

        return []



    print(
        "AIS KEY EXISTS:",
        True,
        "LENGTH:",
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

                "FilterMessageTypes":[
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
                90
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
                                    "UNKNOWN"
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




    except Exception as e:


        print(
            "AIS ERROR:",
            e
        )



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
            "AIS QUALITY: HIGH"
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
