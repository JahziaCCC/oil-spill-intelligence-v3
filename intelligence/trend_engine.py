# intelligence/trend_engine.py

import json
import os
from datetime import datetime, timezone


HISTORY_FILE = "data/risk_history.json"



def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []





def save_history(history):

    os.makedirs(
        "data",
        exist_ok=True
    )


    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            ensure_ascii=False,
            indent=4
        )





def calculate_trend(name, current_score):


    history = load_history()


    previous_scores = []


    for item in history:

        if item.get("name") == name:

            previous_scores.append(
                item.get(
                    "risk_score",
                    0
                )
            )



    trend = "🟢 مستقر"


    change = 0



    if previous_scores:


        last_score = previous_scores[-1]


        change = current_score - last_score



        if change >= 20:

            trend = "🔴 تصاعد خطير"


        elif change >= 10:

            trend = "🟡 ارتفاع"



    history.append(

        {

            "name": name,

            "risk_score": current_score,

            "time": datetime.now(
                timezone.utc
            ).strftime(
                "%Y-%m-%d %H:%M UTC"
            )

        }

    )



    # الاحتفاظ بآخر 500 سجل فقط

    history = history[-500:]



    save_history(history)



    return {

        "trend": trend,

        "change": change

    }
