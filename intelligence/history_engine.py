import json
import os
from datetime import datetime, timezone


HISTORY_FILE = "data/maritime_history.json"



def ensure_storage():

    folder = os.path.dirname(HISTORY_FILE)

    if not os.path.exists(folder):

        os.makedirs(folder)



def save_history(report):

    ensure_storage()


    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M UTC"
    )


    record = {

        "timestamp": timestamp,

        "areas": report

    }


    history = []


    if os.path.exists(HISTORY_FILE):

        try:

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                history = json.load(file)

        except:

            history = []



    history.append(record)



    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            ensure_ascii=False,
            indent=4
        )



def load_history():

    if not os.path.exists(HISTORY_FILE):

        return []


    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)
