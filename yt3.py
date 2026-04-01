# Transcript (Fetching + Normalizing transcript)
from youtube_transcript_api import YouTubeTranscriptApi

def fetch_transcript(video_id, languages=["en"]):
    api = YouTubeTranscriptApi()
    return api.fetch(video_id, languages=languages)

def normalize_transcript(snippets):
    return [
        {
            "text": s.text,
            "start": s.start,
            "end": s.start + s.duration
        }
        for s in snippets
    ]


# print(fetch_transcript("7EWYjFqgmHM")[0])
# print(normalize_transcript(fetch_transcript("7EWYjFqgmHM"))[0])
# print(chunk_transcript(normalize_transcript(fetch_transcript("7EWYjFqgmHM")))[10])