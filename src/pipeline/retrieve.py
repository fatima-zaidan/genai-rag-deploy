# src/pipeline/retrieve.py

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from src.utils.config import DATA_PROCESSED_PATH
from pathlib import Path

def load_vector_store():
    """Loads FAISS index and embeddings."""
    print("🔹 Loading embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

    print("🔹 Loading FAISS index...")
    faiss_path = Path(DATA_PROCESSED_PATH) / "faiss_index_hf"
    vector_store = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store

def retrieve_docs(query: str, k: int = 3):
    """Retrieve top-k most relevant chunks."""
    vector_store = load_vector_store()
    print(f"🔍 Searching for: {query}")
    results = vector_store.similarity_search(query, k=k)

    print("\n🔹 Top results:")
    for i, doc in enumerate(results, 1):
        print(f"\n[{i}] {doc.page_content[:300]}...")  # show first 300 chars

if __name__ == "__main__":
    # Example test query
    query = input("Enter your question: ")
    retrieve_docs(query)
