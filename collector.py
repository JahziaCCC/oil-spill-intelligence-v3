import os
import json
import time
import websocket
from datetime import datetime, timezone


AIS_URL = "wss://stream.aisstream.io/v0/stream"

CACHE_FILE = "cache/ais_cache.json"


API_KEY = os.getenv(
    "AISSTREAM_API_KEY"
)


def save_cache(vessels):

    os.makedirs(
        "cache",
        exist_ok=True
    )


    data = {

        "updated":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "count":
            len(vessels),

        "vessels":
            vessels

    }


    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )



def collect_ais():

    print(
        "📡 AIS Collector Starting..."
    )


    if not API_KEY:

        print(
            "❌ AISSTREAM_API_KEY missing"
        )

        return []



    print(
        "AIS KEY EXISTS:",
        True,
        "LENGTH:",
        len(API_KEY)
    )



    try:


        ws = websocket.create_connection(

            AIS_URL,

            timeout=30

        )


        print(
            "✅ AIS Connected"
        )



        subscribe = {

            "APIKey":
                API_KEY,


            "BoundingBoxes":

            [

                # Strait of Hormuz

                [

                    [25.5,55.0],

                    [27.5,57.0]

                ],


                # Bab Al Mandab

                [

                    [12.0,42.5],

                    [13.5,44.5]

                ],


                # Suez Canal

                [

                    [29.5,31.5],

                    [31.0,33.0]

                ]

            ],


            "FilterMessageTypes":

            [

                "PositionReport"

            ]

        }



        ws.send(

            json.dumps(
                subscribe
            )

        )


        print(
            "✅ Subscription sent"
        )


        print(
            "⏳ Collecting AIS (60 seconds)..."
        )



        vessels = []


        start = time.time()



        while time.time() - start < 60:


            try:


                message = ws.recv()


                data = json.loads(
                    message
                )


                vessel = {


                    "mmsi":

                    data.get(
                        "MMSI"
                    ),


                    "name":

                    data.get(
                        "ShipName",
                        "UNKNOWN"
                    ).strip(),


                    "lat":

                    data.get(
                        "latitude"
                    ),


                    "lon":

                    data.get(
                        "longitude"
                    )

                }


                position = data.get(
                    "PositionReport"
                )


                if position:

                    vessel["speed"] = position.get(
                        "Sog",
                        0
                    )

                    vessel["heading"] = position.get(
                        "Cog",
                        0
                    )


                vessels.append(
                    vessel
                )


                print(
                    "🚢",
                    vessel
                )



            except Exception as e:


                print(
                    "⚠️ Receive Error:",
                    e
                )

                break



        ws.close()



        save_cache(
            vessels
        )


        print(
            "✅ AIS CACHE UPDATED:",
            len(vessels)
        )


        return vessels



    except Exception as e:


        print(
            "❌ AIS Collector Error:",
            e
        )


        return []



if __name__ == "__main__":


    collect_ais()
