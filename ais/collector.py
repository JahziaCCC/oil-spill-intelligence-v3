import os
import json
import asyncio
import websockets
from datetime import datetime


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

AIS_API_KEY = os.getenv("AIS_API_KEY")


def clean_name(name):
    if not name:
        return "UNKNOWN"
    return name.strip()


async def collect_ais_async(duration=120):

    vessels = {}

    print("AIS Collector Starting...")
    print(
        "AIS KEY EXISTS:",
        AIS_API_KEY is not None,
        "LENGTH:",
        len(AIS_API_KEY) if AIS_API_KEY else 0
    )

    if not AIS_API_KEY:
        print("❌ Missing AIS_API_KEY")
        return []

    try:

        async with websockets.connect(
            AISSTREAM_URL,
            ping_interval=20,
            ping_timeout=20
        ) as websocket:

            print("✅ AIS Connected")

            subscription = {
                "APIKey": AIS_API_KEY,
                "BoundingBoxes": [
                    [
                        [-40, -10],
                        [60, 45]
                    ]
                ],
                "FilterMessageTypes": [
                    "PositionReport"
                ]
            }

            await websocket.send(json.dumps(subscription))

            print("✅ Subscription sent")
            print("⏳ Waiting AIS messages...")

            start_time = datetime.utcnow()

            while True:

                try:

                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=10
                    )

                    data = json.loads(message)

                    if data.get("MessageType") != "PositionReport":
                        continue


                    meta = data.get("MetaData", {})
                    position = data.get("Message", {}).get(
                        "PositionReport",
                        {}
                    )


                    mmsi = meta.get("MMSI")

                    if not mmsi:
                        continue


                    vessel = {

                        "mmsi": mmsi,

                        "name": clean_name(
                            meta.get("ShipName")
                        ),

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


                    vessels[mmsi] = vessel


                    print("🚢", vessel)


                    elapsed = (
                        datetime.utcnow()
                        - start_time
                    ).seconds


                    if elapsed >= duration:
                        break


                except asyncio.TimeoutError:
                    continue


    except Exception as e:

        print("❌ AIS ERROR:", e)


    return list(vessels.values())



def collect_ais():

    return asyncio.run(
        collect_ais_async()
    )
