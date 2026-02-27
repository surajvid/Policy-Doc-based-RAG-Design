from app.ingest.chunking import chunk_text

def test_chunk_text_splits_into_multiple_chunks():
    text = "hello " * 1000  # long text
    chunks = chunk_text(text, chunk_size=200, overlap=50)
    assert len(chunks) > 1
    assert chunks[0].text.strip() != ""
