For building a RAG system on top of youtube videos, it tries to solve the level 0 issue (also being one of the major roadblock) of getting chunks in the required format. 

It helps in fetching the transcript of the videos with all the required metadata and chunks in the required format. 

The chunks are created according to the embedding model you will use in the pipeline further.

For an example of the output format, refer to the `aliabdaal5.json` file.

## Requirements

The following external Python libraries are required:
- `yt-dlp` (for fetching video metadata and IDs)
- `youtube-transcript-api` (for fetching transcripts)
- `transformers` (for the tokenizer to chunk the text correctly)

## Usage

You can start the ingestion process by modifying the variables (`CHANNEL_HANDLE`, `MAX_VIDEOS`, etc.) inside `yt8_execute_json.py` and running the script:

```bash
python yt8_execute_json.py
```