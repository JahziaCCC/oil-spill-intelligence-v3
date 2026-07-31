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

    print(
        "📡 AIS Collector Starting..."
    )


    api_key = os.getenv(
        "AISSTREAM_API_KEY"
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



        subscribe_message = {

            "APIKey":

                api_key,


            "BoundingBoxes":

            [

                [

                    [10.0, 30.0],

                    [35.0, 60.0]

                ]

            ],


            "FilterMessageTypes":

            [

                "PositionReport"

            ]

        }



        ws.send(
            json.dumps(
                subscribe_message
            )
        )


        print(
            "✅ Subscription sent"
        )


        print(
            "⏳ Waiting AIS messages..."
        )



        start = time.time()

        printed_sample = False



        while time.time() - start < 60:


            message = ws.recv()


            data = json.loads(
                message
            )


            # طباعة أول رسالة لمعرفة شكلها
            if not printed_sample:

                print(
                    "========== RAW AIS MESSAGE =========="
                )

                print(
                    json.dumps(
                        data,
                        indent=2
                    )
                )

                print(
                    "====================================="
                )

                printed_sample = True



            vessel = {

                "raw": data

            }


            vessels.append(
                vessel
            )


            print(
                "🚢 AIS MESSAGE RECEIVED"
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
        "AIS Vessels Received:",
        len(vessels)
    )


    print(
        "✅ AIS CACHE UPDATED"
    )


    return vessels




if __name__ == "__main__":

    collect_ais()
