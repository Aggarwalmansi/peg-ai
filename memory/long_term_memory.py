# memory/long_term_memory.py

import json
from datetime import datetime

DB_FILE = "memory/scam_memory.json"


def store_event(data: dict):
    """
    Store scam event for learning
    """

    data["timestamp"] = str(datetime.now())

    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
    except:
        db = []

    db.append(data)

    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)