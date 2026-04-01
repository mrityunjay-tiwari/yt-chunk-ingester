# Some way analyzing it
import json
from pathlib import Path

JSON_PATH = Path("aliabdaal.json")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print("No. of videos : ",len(data["videos"]))
print("No. of chunks in last video : ",len(data["videos"][-1]["chunks"]))

videos = data["videos"]

total_duration = sum (
    video["duration_seconds"]
    for video in videos
)

print("Total duration (seconds) : ", total_duration/60)