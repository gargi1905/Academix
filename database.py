import json
import os
from datetime import datetime


FILE = "results.json"


def save_result(username, score, total):

    percentage = round(
        (score / total) * 100,
        2
    )

    result = {

        "username": username,

        "score": score,

        "total": total,

        "percentage": percentage,

        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

    }


    if not os.path.exists(FILE):

        data = []

    else:

        with open(FILE, "r") as f:

            try:

                data = json.load(f)

            except:

                data = []


    data.append(result)


    with open(FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )



def load_results():

    if not os.path.exists(FILE):

        return []


    with open(FILE, "r") as f:

        try:

            return json.load(f)

        except:

            return []