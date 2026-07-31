import os
import json
import asyncio
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

AIS_CACHE_FILE = "data/ais_cache.json"


# المناطق الاستراتيجية
BBOXES = [

    # مضيق هرمز
    [
        [24.0, 54.0],
        [28.0, 60.0]
    ],

    # باب المندب
    [
        [11.0, 40.0],
        [15.0, 45.0]
    ],

    # قناة السويس
    [
        [29.0, 31.0],
        [32.0, 33.5]
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
    print("AIS Collector Starting...")


    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )


    if not api_key:

        print("❌ Missing AISSTREAM_API_KEY")

        return []



    print(
        "AIS KEY EXISTS: True LENGTH:",
        len(api_key)
    )



    vessels = []


    try:

        async with websockets.connect(
            AISSTREAM_URL
        ) as websocket:


            print("✅ AIS Connected")


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


            print("✅ Subscription sent")
            print("⏳ Collecting AIS data...")



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
                        timeout=10
                    )


                    data = json.loads(
                        message
                    )


                    position = (
                        data
                        .get("Message", {})
                        .get("PositionReport")
                    )


                    metadata = (
                        data
                        .get("MetaData", {})
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


                except asyncio.TimeoutError:

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

    print(
        "AIS CACHE UPDATED"
    )

    print("=" * 50)



    return vessels
