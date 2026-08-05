import os
import json
from datetime import datetime, timezone


CACHE_FILE = "data/ais_cache.json"



def save_ais_cache(vessels):

    """
    حفظ آخر بيانات AIS ناجحة
    """

    os.makedirs(
        "data",
        exist_ok=True
    )


    cache_data = {

        "updated":

        datetime.now(
            timezone.utc
        ).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),


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

            cache_data,

            f,

            ensure_ascii=False,

            indent=2

        )




def load_ais_cache():

    """
    استرجاع آخر بيانات AIS محفوظة
    """

    if not os.path.exists(
        CACHE_FILE
    ):

        return []



    try:


        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:


            data = json.load(f)



        vessels = data.get(
            "vessels",
            []
        )



        print(
            "♻️ AIS CACHE LOADED:",
            len(vessels),
            "vessels"
        )



        return vessels



    except Exception as e:


        print(
            "CACHE ERROR:",
            e
        )


        return []




def cache_status():


    if not os.path.exists(
        CACHE_FILE
    ):


        return {

            "status":
            "EMPTY",

            "count":
            0

        }



    try:


        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:


            data = json.load(f)



        return {


            "status":
            "AVAILABLE",


            "count":
            data.get(
                "count",
                0
            ),


            "updated":
            data.get(
                "updated",
                ""
            )

        }


    except:


        return {

            "status":
            "ERROR",

            "count":
            0

        }
