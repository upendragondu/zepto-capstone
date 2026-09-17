from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Paths
BASE_DIR = Path(__file__).resolve().parent
POLICY_DIR = BASE_DIR / "policies"
CHROMA_DIR = BASE_DIR / "chroma_db"


# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Create ChromaDB
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="zepto_policies"
)


def load_policies():
    documents = []
    ids = []

    for file_path in sorted(POLICY_DIR.glob("*.txt")):
        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(text)
        ids.append(file_path.stem)

    return documents, ids


def build_vector_store():
    documents, ids = load_policies()

    embeddings = embedding_model.encode(
        documents
    ).tolist()

    # Avoid duplicate data when running again
    if collection.count() > 0:
        collection.delete(
            ids=collection.get()["ids"]
        )

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    print(f"Added {len(documents)} policy documents to ChromaDB.")


def search_policies(query, top_k=3):
    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results