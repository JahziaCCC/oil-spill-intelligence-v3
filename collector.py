import os
import json
import time
import websocket
from datetime import datetime, timezone


AIS_URL = "wss://stream.aisstream.io/v0/stream"

CACHE_FILE = "cache/ais_cache.json"


API_KEY = os.getenv("AISSTREAM_API_KEY")


def save_cache(vessels):

    data = {
        "updated": datetime.now(
            timezone.utc
        ).isoformat(),

        "count": len(vessels),

        "vessels": vessels
    }


    os.makedirs(
        "cache",
        exist_ok=True
    )


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



print(
    "AIS KEY EXISTS:",
    API_KEY is not None
)


if not API_KEY:

    raise Exception(
        "AISSTREAM_API_KEY missing"
    )



print(
    "📡 Connecting AISStream..."
)


ws = websocket.create_connection(
    AIS_URL,
    timeout=30
)


print(
    "✅ AIS Connected"
)



subscribe = {

    "APIKey": API_KEY,

    "BoundingBoxes": [

        [
            [25.5,55.0],
            [27.5,57.0]
        ],

        [
            [12.0,42.5],
            [13.5,44.5]
        ],

        [
            [29.5,31.5],
            [31.0,33.0]
        ]

    ]

}


ws.send(
    json.dumps(subscribe)
)


print(
    "✅ Subscription sent"
)


print(
    "⏳ Collecting AIS for 60 seconds..."
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
            data.get("MMSI"),

            "name":
            data.get(
                "ShipName",
                "UNKNOWN"
            ),

            "lat":
            data.get(
                "latitude"
            ),

            "lon":
            data.get(
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


    except Exception as e:

        print(
            "Receive error:",
            e
        )

        break



save_cache(
    vessels
)


print(
    "✅ AIS CACHE UPDATED:",
    len(vessels)
)


ws.close()
