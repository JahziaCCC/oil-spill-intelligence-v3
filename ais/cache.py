import os
import json
from datetime import datetime, timezone


CACHE_FILE = "data/ais_cache.json"



def save_ais_cache(vessels):

    os.makedirs(
        "data",
        exist_ok=True
    )


    cache = {

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
    ) as file:


        json.dump(
            cache,
            file,
            ensure_ascii=False,
            indent=2
        )


    print(
        "✅ AIS CACHE SAVED"
    )




def load_ais_cache():


    # إنشاء ملف فارغ أول مرة

    if not os.path.exists(
        CACHE_FILE
    ):


        os.makedirs(
            "data",
            exist_ok=True
        )


        empty_cache = {

            "updated":

            datetime.now(
                timezone.utc
            ).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            ),


            "count": 0,


            "vessels": []

        }



        with open(
            CACHE_FILE,
            "w",
            encoding="utf-8"
        ) as file:


            json.dump(
                empty_cache,
                file,
                ensure_ascii=False,
                indent=2
            )



        print(
            "🆕 AIS CACHE CREATED"
        )


        return []



    try:


        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:


            data = json.load(file)



        vessels = data.get(
            "vessels",
            []
        )



        if vessels:


            print(
                "♻️ AIS CACHE LOADED:",
                len(vessels),
                "vessels"
            )


        else:


            print(
                "⚠️ AIS CACHE EMPTY"
            )



        return vessels



    except Exception as e:


        print(
            "CACHE ERROR:",
            e
        )


        return []




def get_cache_info():


    if not os.path.exists(
        CACHE_FILE
    ):


        return {

            "status":
            "MISSING",

            "count":
            0

        }



    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as file:


        data = json.load(file)



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
