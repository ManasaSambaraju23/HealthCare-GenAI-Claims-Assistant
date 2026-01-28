def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150
) -> list:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks
