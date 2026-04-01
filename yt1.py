# Getting video_ids from channel
from yt_dlp import YoutubeDL

def get_latest_video_ids(channel_handle, max_videos):
    channel_videos_url = f"https://www.youtube.com/@{channel_handle}/videos"

    ydl_opts = {
        "extract_flat": True,
        "skip_download": True,
        "playlistend": max_videos,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_videos_url, download=False)

    return [
        entry.get("id")
        for entry in info.get("entries", [])
        if entry.get("id")
    ]

# print(get_latest_video_ids("TaarakMehtaKaOoltahChashmah", 10))

