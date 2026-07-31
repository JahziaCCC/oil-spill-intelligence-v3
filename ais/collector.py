import os
import json
import asyncio
from datetime import datetime

import websockets


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

AIS_CACHE_FILE = "data/ais_cache.json"


def save_cache(vessels):
    os.makedirs("data", exist_ok=True)

    with open(AIS_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            vessels,
            f,
            ensure_ascii=False,
            indent=2
        )


async def collect_ais(duration=120):

    print("AIS Collector Starting...")

    api_key = os.getenv("AISSTREAM_API_KEY")

    print(
        f"AIS KEY EXISTS: {bool(api_key)} LENGTH: {len(api_key) if api_key else 0}"
    )

    if not api_key:
        print("❌ Missing AISSTREAM_API_KEY")
        return []

    vessels = {}

    subscription = {
        "APIKey": api_key,
        "BoundingBoxes": [
            [
                [20, 20],
                [60, 45]
            ]
        ],
        "FilterMessageTypes": [
            "PositionReport"
        ]
    }


    try:

        async with websockets.connect(
            AISSTREAM_URL,
            ping_interval=None
        ) as websocket:


            print("✅ AIS Connected")


            await websocket.send(
                json.dumps(subscription)
            )


            print("✅ Subscription sent")
            print("⏳ Collecting AIS data...")


            start = datetime.utcnow()


            while True:

                try:

                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=10
                    )


                    data = json.loads(message)


                    meta = data.get(
                        "MetaData",
                        {}
                    )


                    position = data.get(
                        "Message",
                        {}
                    ).get(
                        "PositionReport",
                        {}
                    )


                    mmsi = meta.get(
                        "MMSI"
                    )


                    if not mmsi:
                        continue


                    vessel = {

                        "mmsi": mmsi,

                        "name": meta.get(
                            "ShipName",
                            "UNKNOWN"
                        ).strip(),

                        "lat": position.get(
                            "Latitude"
                        ),

                        "lon": position.get(
                            "Longitude"
                        ),

                        "speed": position.get(
                            "Sog",
                            0
                        ),

                        "heading": position.get(
                            "TrueHeading",
                            0
                        ),

                        "timestamp": meta.get(
                            "time_utc"
                        )

                    }


                    vessels[str(mmsi)] = vessel


                    if (
                        datetime.utcnow()
                        -
                        start
                    ).seconds >= duration:

                        break


                except asyncio.TimeoutError:

                    continue



    except Exception as e:

        print(
            "AIS ERROR:",
            e
        )



    result = list(
        vessels.values()
    )


    save_cache(result)


    print()
    print("="*50)
    print("AIS SUMMARY")
    print("="*50)

    print(
        "AIS Vessels Received:",
        len(result)
    )

    print(
        "AIS CACHE UPDATED"
    )

    print("="*50)


    return result
