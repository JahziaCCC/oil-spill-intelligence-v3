# intelligence/history_engine.py

# Strategic Maritime Historical Trend Engine V6

import json
import os
from datetime import datetime, timezone


HISTORY_FILE = "data/maritime_history.json"



def ensure_storage():

    folder = os.path.dirname(HISTORY_FILE)

    if folder and not os.path.exists(folder):

        os.makedirs(folder)





def load_history():

    ensure_storage()


    if not os.path.exists(HISTORY_FILE):

        return []


    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except:

        return []






def save_history(report):


    ensure_storage()


    history = load_history()



    record = {


        "time":
            datetime.now(
                timezone.utc
            ).strftime(
                "%Y-%m-%d %H:%M UTC"
            ),


        "areas":
            report

    }



    history.append(record)



    # الاحتفاظ بآخر 100 قراءة

    history = history[-100:]



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



    return record






def analyze_trend(report):


    history = load_history()



    trend = {}



    for area,data in report.items():


        current = data.get(
            "risk_score",
            0
        )


        previous = current



        if history:


            try:

                previous = history[-1]["areas"][area].get(
                    "risk_score",
                    current
                )

            except:

                previous = current





        difference = current - previous





        if difference >= 20:

            direction = "🔺 تصاعد سريع"


        elif difference > 0:

            direction = "↗️ ارتفاع"


        elif difference < 0:

            direction = "↘️ انخفاض"


        else:

            direction = "⚪ مستقر"





        trend[area] = {


            "current":

                current,


            "previous":

                previous,


            "difference":

                difference,


            "trend":

                direction

        }




    save_history(report)



    return trend
