# Building Video Object
def build_video_object(video_id, metadata, chunks):
    return {
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": metadata.get("title"),
        "description": metadata.get("description"),
        "published_at": metadata.get("published_at"),
        "duration_seconds": metadata.get("duration_seconds"),
        "chunks": [
            {
                **chunk,
                "chunk_id": f"{video_id}_{chunk['chunk_id']}"
            }
            for chunk in chunks
        ]
    }
