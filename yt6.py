# Building Channel Object
from datetime import datetime

def build_channel_object(channel_handle, videos):
    return {
        "channel": {
            "handle": channel_handle,
            "channel_url": f"https://www.youtube.com/@{channel_handle}",
            "ingested_at": datetime.utcnow().isoformat() + "Z"
        },
        "videos": videos
    }
