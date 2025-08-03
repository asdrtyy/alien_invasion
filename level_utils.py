import json
import os


SAVE_FILE = "unlocked_levels.json"


def save_unlocked_levels(level):
    data = {"unlocked_levels": level}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def load_unlocked_levels():
    if not os.path.exists(SAVE_FILE):
        return 1  # минимум 1 уровень всегда разблокирован
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
        return data.get("unlocked_levels", 1)
