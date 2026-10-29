import ollama
import chromadb
from sentence_transformers import SentenceTransformer

MODEL = "llama3.2"  # use "llama3.2:1b" if you downloaded the small one

model = SentenceTransformer("all-MiniLM-L6-v2")
col = chromadb.PersistentClient(path="db").get_or_create_collection("notes")

SYSTEM = (
    "You are a study assistant. Answer ONLY using the provided context. "
    "Cite sources like [1], [2]. If the context doesn't contain the answer, "
    "say you can't find it in the notes. Explain clearly, as a tutor would."
)


def retrieve(question: str, k: int = 4):
    emb = model.encode([question]).tolist()
    res = col.query(query_embeddings=emb, n_results=k)
    return [
        {"text": d, "source": m["source"], "page": m["page"]}
        for d, m in zip(res["documents"][0], res["metadatas"][0])
    ]


def answer(question: str, k: int = 4):
    hits = retrieve(question, k)
    context = "\n\n".join(
        f"[{i+1}] ({h['source']}, p.{h['page']})\n{h['text']}" for i, h in enumerate(hits)
    )
    resp = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return resp["message"]["content"], hits