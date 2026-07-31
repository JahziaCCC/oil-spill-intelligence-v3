import os
import json
import time
import websocket
from datetime import datetime, timezone


AIS_URL = "wss://stream.aisstream.io/v0/stream"

CACHE_FILE = "cache/ais_cache.json"


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

    api_key = os.getenv(
        "AISSTREAM_API_KEY"
    )


    print(
        "📡 AIS Collector Starting..."
    )


    if not api_key:

        print(
            "❌ AISSTREAM_API_KEY missing"
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

        ws = websocket.create_connection(

            AIS_URL,

            timeout=30

        )


        print(
            "✅ AIS Connected"
        )



        subscribe = {

            "APIKey": api_key,


            "BoundingBoxes":

            [

                [

                    [25.5,55.0],

                    [27.5,57.0]

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


        start = time.time()


        print(
            "⏳ Waiting AIS messages..."
        )


        while time.time() - start < 120:


            message = ws.recv()


            data = json.loads(
                message
            )


            vessel = {


                "mmsi":
                    data.get("MMSI"),


                "name":
                    data.get(
                        "ShipName",
                        "UNKNOWN"
                    ).strip(),


                "lat":
                    data.get("latitude"),


                "lon":
                    data.get("longitude")

            }


            vessels.append(
                vessel
            )


            print(
                "🚢",
                vessel
            )



        ws.close()



    except Exception as e:

        print(
            "❌ AIS Error:",
            e
        )



    save_cache(
        vessels
    )


    print(
        "✅ AIS CACHE UPDATED:",
        len(vessels)
    )


    return vessels



if __name__ == "__main__":

    collect_ais()
