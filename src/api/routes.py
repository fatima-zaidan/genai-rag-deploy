from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api.schemas import QueryRequest, QueryResponse
from src.api.services import create_query, get_queries, delete_query
from src.database.dependencies import get_db
from src.pipeline.generate import build_qa_chain
from src.utils.logger import get_logger
from typing import List

router = APIRouter()
logger = get_logger(__name__)
qa_chain = build_qa_chain()

@router.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        result = qa_chain.invoke({"query": request.question})
        answer = result["result"]

        create_query(db, request.question, answer)

        sources = [
            doc.page_content[:150].replace("\n", " ") + "..."
            for doc in result.get("source_documents", [])
        ]

        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        logger.exception("Error while processing query")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/queries", response_model=List[QueryResponse])
def read_queries(db: Session = Depends(get_db)):
    records = get_queries(db)
    return [QueryResponse(answer=r.answer, sources=[]) for r in records]


@router.delete("/queries/{query_id}")
def delete_query_entry(query_id: int, db: Session = Depends(get_db)):
    success = delete_query(db, query_id)
    if not success:
        raise HTTPException(status_code=404, detail="Query not found")
    return {"message": "Deleted successfully"}
