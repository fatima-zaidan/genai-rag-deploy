import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from src.utils.config import DATA_PROCESSED_PATH, OPENAI_API_KEY
from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_vector_store():
    """Load FAISS vector store with the same embedding model used before."""
    logger.info("🔹 Loading embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

    faiss_path = Path(DATA_PROCESSED_PATH) / "faiss_index_hf"
    if not faiss_path.exists():
        logger.error(f"FAISS index not found at {faiss_path}")
        raise FileNotFoundError("FAISS index not found. Please run the embedding step first.")
    vector_store = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
    logger.info("✅ FAISS index loaded successfully.")
    return vector_store

def build_qa_chain():
    """Connect retriever with OpenAI model."""
    retriever = load_vector_store().as_retriever(search_kwargs={"k": 3})
    logger.info("🔹 Retrieval created with top 3 chunks")
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        openai_api_key=OPENAI_API_KEY
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are an expert AI assistant. Use the following context to answer the question accurately.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer clearly and concisely based only on the provided context."
        ),
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    return chain

def run_generation():
      """Interactive Q&A loop."""
      logger.info("RAG generation started. Type 'exit' to quit.")
      qa_chain = build_qa_chain()
      print("💬 Ask me anything based on your data! (type 'exit' to quit)\n")

      while True:
        query = input("🧠 Your question: ").strip()
        if query.lower() in ["exit", "quit"]:
            logger.info("User exited the RAG loop.")
            break

        logger.info(f"Query: {query}")

        try:
            result = qa_chain.invoke({"query": query})
            answer = result["result"]
            retrieved_docs = result["source_documents"]

            # Log the answer
            logger.info(f"Answer: {answer}")

            # Log retrieved chunks (first 150 chars)
            for i, doc in enumerate(retrieved_docs):
                snippet = doc.page_content[:150].replace("\n", " ")
                logger.info(f"Retrieved chunk {i+1}: {snippet}")

            # Optional: console output
            print("\n🤖 Answer:")
            print(answer)
            print("\n📚 Sources:")
            for doc in retrieved_docs:
                print("-", doc.page_content[:150].replace("\n", " ") + "...")
            print("-" * 60)

        except Exception as e:
            logger.error(f"Error during query: {e}")
            print("❌ Error generating answer. Check logs for details.")


if __name__ == "__main__":
    run_generation()