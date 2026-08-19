import os
import glob
import numpy as np
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

KNOWLEDGE_BASE_DIR = "knowledge_base"
EMBEDDING_MODEL = "gemini-embedding-001"

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def load_chunks():
    """Read every .txt file in the knowledge base and split each into chunks."""
    chunks = []
    file_paths = sorted(glob.glob(os.path.join(KNOWLEDGE_BASE_DIR, "*.txt")))
    for file_path in file_paths:
        with open(file_path, "r") as f:
            content = f.read()
        sections = [s.strip() for s in content.split("\n\n") if s.strip()]
        for section in sections:
            chunks.append({"text": section, "source": os.path.basename(file_path)})
    return chunks


def embed_texts(texts, task_type):
    """Call the Gemini embedding model on a list of strings."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return [embedding.values for embedding in response.embeddings]


def build_index():
    """Embed every chunk once and attach its vector, forming the searchable index."""
    chunks = load_chunks()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts, task_type="RETRIEVAL_DOCUMENT")
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = np.array(embedding)
    return chunks


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query, index, top_k=3):
    """Embed the query and return the top_k most similar chunks from the index."""
    query_embedding = np.array(embed_texts([query], task_type="RETRIEVAL_QUERY")[0])
    scored = [
        (cosine_similarity(query_embedding, chunk["embedding"]), chunk)
        for chunk in index
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]


if __name__ == "__main__":
    print("Building knowledge base index...")
    index = build_index()
    print(f"Indexed {len(index)} chunks from '{KNOWLEDGE_BASE_DIR}/'\n")

    while True:
        query = input("Ask a question (or 'quit'): ").strip()
        if query.lower() in ["quit", "exit"]:
            break
        results = retrieve(query, index)
        print("\nTop matches:")
        for rank, chunk in enumerate(results, start=1):
            print(f"{rank}. [{chunk['source']}] {chunk['text'][:150]}...")
        print()
