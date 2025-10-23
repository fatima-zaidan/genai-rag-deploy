import pytest
from src.pipeline.generate import build_qa_chain

def test_rag_pipeline():
    """Test the end-to-end RAG pipeline."""
    qa_chain = build_qa_chain()
    assert qa_chain is not None, "QA chain failed to initialize."

    # Valid query
    result = qa_chain.invoke({"query": "What is Retrieval-Augmented Generation?"})
    assert "result" in result and len(result["result"].strip()) > 0, "Empty or missing answer."
    assert len(result.get("source_documents", [])) > 0, "No sources retrieved."

    # Invalid query (should not crash)
    bad_query = qa_chain.invoke({"query": "asdkjashdkjahsdkj"})
    assert "result" in bad_query, "Pipeline failed on invalid query."
