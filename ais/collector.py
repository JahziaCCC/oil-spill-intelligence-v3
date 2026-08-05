import os
import json
import asyncio
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"


BBOXES = [
    [
        [8.0, 38.0],
        [33.0, 62.0]
    ]
]


async def collect_ais():

    print()
    print("=" * 60)
    print("تشغيل AIS Collector V8 TEST MODE")
    print("=" * 60)


    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )


    if not api_key:

        print("❌ AIS KEY MISSING")
        return []



    print(
        "AIS KEY LENGTH:",
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

                "BoundingBoxes": BBOXES

            }


            await websocket.send(
                json.dumps(subscription)
            )


            print(
                "✅ Subscription sent"
            )


            print(
                "⏳ Waiting AIS messages..."
            )



            counter = 0


            while counter < 30:


                try:

                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=10
                    )


                    data = json.loads(
                        message
                    )


                    print(
                        "📡 MESSAGE TYPE:",
                        data.get("MessageType")
                    )


                    print(
                        "RAW KEYS:",
                        data.keys()
                    )



                    if "MetaData" in data:


                        meta = data["MetaData"]


                        vessel = {

                            "mmsi":
                            meta.get("MMSI"),

                            "name":
                            meta.get(
                                "ShipName",
                                ""
                            ),

                            "lat":
                            meta.get(
                                "latitude"
                            ),

                            "lon":
                            meta.get(
                                "longitude"
                            )

                        }


                        vessels.append(
                            vessel
                        )


                        print(
                            "🚢",
                            vessel
                        )


                except asyncio.TimeoutError:

                    print(
                        "⏳ Waiting..."
                    )


                counter += 1



    except Exception as e:

        print(
            "AIS ERROR:",
            e
        )



    print()
    print("="*50)
    print(
        "AIS RECEIVED:",
        len(vessels)
    )
    print("="*50)



    return vessels
