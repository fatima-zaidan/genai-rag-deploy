from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from pathlib import Path
from src.utils.config import DATA_PROCESSED_PATH

# Load processed chunks
processed_file = Path(DATA_PROCESSED_PATH) / "processed.txt"
with open(processed_file, "r", encoding="utf-8") as f:
    chunks = [line.strip() for line in f if line.strip()]

# Initialize HF embeddings (local)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS vector store
vector_store = FAISS.from_texts(chunks, embeddings)

# Save locally
faiss_path = Path(DATA_PROCESSED_PATH) / "faiss_index_hf"
vector_store.save_local(faiss_path)

print(f"✅ Hugging Face embeddings saved to {faiss_path}")

