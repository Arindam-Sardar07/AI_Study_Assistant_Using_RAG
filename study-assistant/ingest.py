from pathlib import Path
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

CHUNK_SIZE, OVERLAP = 800, 150

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="db")
col = client.get_or_create_collection("notes", metadata={"hnsw:space": "cosine"})


def read_file(path: Path):
    """Return a list of (page_number, text)."""
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return [(i + 1, p.extract_text() or "") for i, p in enumerate(reader.pages)]
    return [(1, path.read_text(encoding="utf-8"))]


def chunk(text: str):
    step = CHUNK_SIZE - OVERLAP
    pieces = (text[i:i + CHUNK_SIZE] for i in range(0, len(text), step))
    return [p for p in pieces if p.strip()]


def main():
    for path in Path("data").glob("*"):
        if path.suffix.lower() not in {".pdf", ".txt", ".md"}:
            continue
        ids, docs, metas = [], [], []
        for page, text in read_file(path):
            for n, c in enumerate(chunk(text)):
                ids.append(f"{path.name}-{page}-{n}")
                docs.append(c)
                metas.append({"source": path.name, "page": page})
        if docs:
            embeddings = model.encode(docs).tolist()
            col.upsert(ids=ids, documents=docs, embeddings=embeddings, metadatas=metas)
            print(f"Indexed {path.name}: {len(docs)} chunks")


if __name__ == "__main__":
    main()