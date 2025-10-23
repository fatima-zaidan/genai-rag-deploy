from fastapi import FastAPI
from src.database.session import engine, Base
from src.database import models_db
from src.api.routes import router as queries_router
from src.utils.logger import get_logger

app = FastAPI(title="RAG API with PostgreSQL")
logger = get_logger(__name__)

# ✅ Create all tables on startup
Base.metadata.create_all(bind=engine)

# ✅ Include API router
app.include_router(queries_router, prefix="/api", tags=["Queries"])

@app.get("/")
def root():
    return {"message": "Welcome to the RAG API 🚀"}
