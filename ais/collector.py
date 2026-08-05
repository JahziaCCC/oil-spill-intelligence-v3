import os
import json
import asyncio
import websockets
from datetime import datetime, timezone


AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"

AIS_CACHE_FILE = "data/ais_cache.json"

AIS_STATUS_FILE = "data/ais_status.json"


BBOXES = [

    [
        [22.0, 50.0],
        [30.0, 62.0]
    ],

    [
        [8.0, 38.0],
        [16.0, 47.0]
    ],

    [
        [27.0, 29.0],
        [33.0, 35.0]
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




def load_cache():

    if not os.path.exists(
        AIS_CACHE_FILE
    ):

        return []


    try:

        with open(
            AIS_CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    except:

        return []




def save_status(status):

    os.makedirs(
        "data",
        exist_ok=True
    )


    with open(
        AIS_STATUS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            status,
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
            "❌ AIS API KEY غير موجود"
        )

        return load_cache()



    print(
        "AIS KEY EXISTS: True LENGTH:",
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

                "FilterMessageTypes":
                [
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



                        print(
                            "🚢",
                            vessel["name"],
                            "|",
                            vessel["lat"],
                            vessel["lon"]
                        )



                except asyncio.TimeoutError:

                    continue





    except Exception as e:


        print(
            "AIS ERROR:",
            e
        )





    # =========================
    # Data Quality Logic
    # =========================


    now = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M UTC"
    )



    if len(vessels) > 0:


        save_cache(
            vessels
        )


        status = {

            "status":
            "ONLINE",

            "quality":
            "HIGH",

            "source":
            "AIS REAL TIME",

            "vessels":
            len(vessels),

            "last_update":
            now

        }



    else:


        cached = load_cache()



        if cached:


            vessels = cached


            status = {

                "status":
                "DEGRADED",

                "quality":
                "MEDIUM",

                "source":
                "AIS CACHE",

                "vessels":
                len(vessels),

                "last_update":
                now

            }


            print(
                "⚠️ Using previous AIS cache"
            )



        else:


            status = {

                "status":
                "OFFLINE",

                "quality":
                "LOW",

                "source":
                "NO DATA",

                "vessels":
                0,

                "last_update":
                now

            }





    save_status(
        status
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
        "AIS DATA STATUS:",
        status["status"]
    )


    print(
        "AIS QUALITY:",
        status["quality"]
    )


    print("=" * 50)



    return vessels
