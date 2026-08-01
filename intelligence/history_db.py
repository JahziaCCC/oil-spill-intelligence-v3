import sqlite3
from datetime import datetime, timezone


DB_NAME = "maritime_history.db"



def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS risk_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            area TEXT,

            ships INTEGER,

            tankers INTEGER,

            strategic INTEGER,

            moving INTEGER,

            stopped INTEGER,

            risk_score INTEGER

        )
        """
    )


    conn.commit()

    conn.close()





def save_report(report):


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()



    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M UTC"
    )



    for area,data in report.items():


        cursor.execute(

            """
            INSERT INTO risk_history
            (
                timestamp,
                area,
                ships,
                tankers,
                strategic,
                moving,
                stopped,
                risk_score
            )

            VALUES (?,?,?,?,?,?,?,?)

            """,

            (

                timestamp,

                area,

                data.get(
                    "ships",
                    0
                ),

                data.get(
                    "tankers",
                    0
                ),

                data.get(
                    "strategic",
                    0
                ),

                data.get(
                    "moving",
                    0
                ),

                data.get(
                    "stopped",
                    0
                ),

                data.get(
                    "risk_score",
                    0
                )

            )

        )



    conn.commit()

    conn.close()




def get_previous_score(area):


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()



    cursor.execute(

        """
        SELECT risk_score

        FROM risk_history

        WHERE area=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (area,)

    )


    result = cursor.fetchone()


    conn.close()



    if result:

        return result[0]


    return None
