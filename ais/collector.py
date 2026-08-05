import os
import json
import asyncio
import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

AIS_CACHE_FILE = "data/ais_cache.json"


async def collect_ais():

    print()
    print("=" * 60)
    print("تشغيل AIS Collector GLOBAL DIAGNOSTIC MODE")
    print("=" * 60)


    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )


    if not api_key:

        print("❌ AIS KEY NOT FOUND")
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

                "FilterMessageTypes": [
                    "PositionReport"
                ]

            }


            await websocket.send(
                json.dumps(subscription)
            )


            print(
                "✅ GLOBAL SUBSCRIPTION SENT"
            )


            timeout = 60

            start = asyncio.get_event_loop().time()


            while (
                asyncio.get_event_loop().time()
                -
                start
                <
                timeout
            ):


                try:

                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=10
                    )


                    data = json.loads(
                        message
                    )


                    metadata = data.get(
                        "MetaData",
                        {}
                    )


                    position = data.get(
                        "Message",
                        {}
                    ).get(
                        "PositionReport"
                    )


                    if position:


                        vessel = {

                            "mmsi":
                            metadata.get("MMSI"),


                            "name":
                            metadata.get(
                                "ShipName",
                                ""
                            ),


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
                            )

                        }


                        vessels.append(
                            vessel
                        )


                        print(
                            "🚢",
                            vessel["name"],
                            vessel["lat"],
                            vessel["lon"]
                        )


                except asyncio.TimeoutError:

                    print(
                        "⏳ Waiting AIS message..."
                    )


    except Exception as e:

        print(
            "AIS ERROR:",
            e
        )


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


    print()
    print("=" * 60)
    print(
        "AIS RECEIVED:",
        len(vessels)
    )
    print("=" * 60)


    return vessels
