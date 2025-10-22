# src/database/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from src.database.session import Base



class QueryRecord(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
