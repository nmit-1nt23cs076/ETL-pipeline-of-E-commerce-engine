import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Database & Storage Paths
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", str(DATA_DIR / "ecommerce.db"))
if not Path(SQLITE_DB_PATH).is_absolute():
    SQLITE_DB_PATH = str(BASE_DIR / SQLITE_DB_PATH)

VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", str(BASE_DIR / "vectorstore"))
if not Path(VECTOR_STORE_DIR).is_absolute():
    VECTOR_STORE_DIR = str(BASE_DIR / VECTOR_STORE_DIR)

# API Keys & LLM Config
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-4")

# ETL Defaults
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "True").lower() in ("true", "1", "yes")

# Embedding Model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_COLLECTION_NAME = "ecommerce_reviews"
