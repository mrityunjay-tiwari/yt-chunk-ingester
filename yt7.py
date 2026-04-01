# Saving to a json file
import json

def save_channel_to_json(channel_data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(channel_data, f, ensure_ascii=False, indent=2)
