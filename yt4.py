# Chunking (snippets to tokens)
from transformers import AutoTokenizer

print("Loading nvidia/llama-nemotron-embed-vl-1b-v2 tokenizer...")
# I did initialize it once when this module is imported, so it doesn't reload per video.
tokenizer = AutoTokenizer.from_pretrained("nvidia/llama-nemotron-embed-vl-1b-v2")

def chunk_transcript(snippets, max_tokens=350, overlap_tokens=50):
    chunks = []
    current_snippets = []
    current_token_count = 0
    chunk_index = 0
    
    i = 0
    while i < len(snippets):
        s = snippets[i]
        text = s["text"].strip()
        
        if not text:
            i += 1
            continue
            
        # Tokenize to get the exact Llama-Nemotron token count
        tokens = tokenizer.encode(text, add_special_tokens=False)
        snippet_token_count = len(tokens)
        
        current_snippets.append({
            "snippet": s,
            "token_count": snippet_token_count
        })
        current_token_count += snippet_token_count
        
        # chunk size rate limit
        if current_token_count >= max_tokens:
            chunk_start = current_snippets[0]["snippet"]["start"]
            last_end = current_snippets[-1]["snippet"]["end"]
            chunk_text = " ".join([cs["snippet"]["text"].strip() for cs in current_snippets])
            
            chunks.append({
                "chunk_id": str(chunk_index),
                "text": chunk_text,
                "start": chunk_start,
                "end": last_end
            })
            chunk_index += 1

            while current_token_count > overlap_tokens and len(current_snippets) > 1:
                removed_cs = current_snippets.pop(0)
                current_token_count -= removed_cs["token_count"]
                
        i += 1

    if current_snippets and current_token_count > 0:
        chunk_start = current_snippets[0]["snippet"]["start"]
        last_end = current_snippets[-1]["snippet"]["end"]
        chunk_text = " ".join([cs["snippet"]["text"].strip() for cs in current_snippets])
        
        # last overlap check sth sth
        if not chunks or chunks[-1]["text"] != chunk_text:
            chunks.append({
                "chunk_id": str(chunk_index),
                "text": chunk_text,
                "start": chunk_start,
                "end": last_end
            })

    return chunks
