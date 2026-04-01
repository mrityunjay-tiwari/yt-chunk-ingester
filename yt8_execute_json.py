import json
import time
import random
from datetime import datetime, timezone
from pathlib import Path

from yt1 import get_latest_video_ids
from yt2 import get_video_metadata
from yt3 import fetch_transcript, normalize_transcript
from yt4 import chunk_transcript
from yt7 import save_channel_to_json

CHANNEL_HANDLE = "aliabdaal"
OUTPUT_FILE = "aliabdaal5.json"

MAX_VIDEOS = 5          
BASE_DELAY_SECONDS = 10.0     
JITTER_RANGE = (1.0, 3.0)     

def load_existing_data(path: str):
    if not Path(path).exists():
        return None, set()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    processed_ids = {
        video["video_id"]
        for video in data.get("videos", [])
        if video.get("transcript_status") == "ok"
    }

    return data, processed_ids


def polite_sleep():
    delay = BASE_DELAY_SECONDS + random.uniform(*JITTER_RANGE)
    print(f"Sleeping {delay:.1f}s")
    time.sleep(delay)


def ingest_channel(channel_handle, max_videos, output_file):
    print(f"Starting ingestion for @{channel_handle}")

    # Existing progress load keep the track 
    existing_data, processed_ids = load_existing_data(output_file)

    if existing_data:
        print(f"Resuming from existing file ({len(processed_ids)} videos already processed)")
        videos = existing_data["videos"]
    else:
        videos = []

    video_ids = get_latest_video_ids(channel_handle, max_videos)
    print(f"Discovered {len(video_ids)} videos")

    channel_data = {
        "channel": {
            "handle": channel_handle,
            "channel_url": f"https://www.youtube.com/@{channel_handle}",
            "ingested_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        },
        "videos": videos
    }

    for index, video_id in enumerate(video_ids, start=1):
        if video_id in processed_ids:
            print(f"[{index}/{len(video_ids)}] Skipping {video_id} (already processed)")
            continue

        print(f"[{index}/{len(video_ids)}] Processing {video_id}")

        try:
            metadata = get_video_metadata(video_id)
        except Exception as e:
            print(f"Metadata failed for {video_id}: {e}")
            continue

        chunks = []
        transcript_status = "blocked"

        try:
            print("Fetching transcript...")
            raw = fetch_transcript(video_id)
            normalized = normalize_transcript(raw)
            chunks = chunk_transcript(normalized)
            transcript_status = "ok"
            print(f"Transcript OK ({len(chunks)} chunks)")

        except Exception as e:
            print(f"Transcript blocked for {video_id}: {e}")

        video_object = {
            **metadata,
            "chunks": [
                {
                    **chunk,
                    "chunk_id": f"{video_id}_{chunk['chunk_id']}"
                }
                for chunk in chunks
            ],
            "transcript_status": transcript_status
        }

        videos.append(video_object)

        channel_data = {
            "channel": {
                "handle": channel_handle,
                "channel_url": f"https://www.youtube.com/@{channel_handle}",
                "ingested_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            },
            "videos": videos
        }

        save_channel_to_json(channel_data, output_file)

        # Rate limit
        polite_sleep()

    print("Ingestion completed")
    return channel_data

if __name__ == "__main__":
    ingest_channel(
        channel_handle=CHANNEL_HANDLE,
        max_videos=MAX_VIDEOS,
        output_file=OUTPUT_FILE
    )
