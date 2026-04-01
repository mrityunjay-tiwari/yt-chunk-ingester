# Metadata (Per-Video Metadata)
from yt_dlp import YoutubeDL

def get_video_metadata(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"

    with YoutubeDL({"skip_download": True}) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "video_id": video_id,
        "url": url,
        "title": info.get("title"),
        # "description": info.get("description"),
        "published_at": info.get("upload_date"),
        "duration_seconds": info.get("duration"),
    }

# print(get_video_metadata("nH0M01xeP2g"))
