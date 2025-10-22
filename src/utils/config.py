import os
from dotenv import load_dotenv

load_dotenv()

DATA_RAW_PATH = os.getenv("DATA_RAW_PATH", "data/raw")
DATA_PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH", "data/processed")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))  # adjust later if needed
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")