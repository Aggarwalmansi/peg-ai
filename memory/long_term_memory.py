# memory/long_term_memory.py

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "scam_memory.json"
MAX_EVENTS = 500


def store_event(data: dict):
    """
    Store scam event for learning
    """

    data["timestamp"] = str(datetime.now())

    try:
        with DB_FILE.open("r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception:
        db = []

    db.append(data)
    db = db[-MAX_EVENTS:]

    with DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
