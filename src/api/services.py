from typing import List

from sqlalchemy.orm import Session
from src.database.models_db import QueryRecord


def create_query(db: Session, question: str, answer: str):
    new_query = QueryRecord(question=question, answer=answer)
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

def get_queries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(QueryRecord).offset(skip).limit(limit).all()

def delete_query(db: Session, query_id: int):
    record = db.query(QueryRecord).filter(QueryRecord.id == query_id).first()
    if record:
        db.delete(record)
        db.commit()
        return True
    return False