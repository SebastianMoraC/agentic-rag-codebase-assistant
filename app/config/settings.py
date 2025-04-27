from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "vectordb")

DB_CONNECTION_STRING = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

OPENAI_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-small"

RELEVANCE_THRESHOLD = 0.8

DATA_DIR.mkdir(parents=True, exist_ok=True)
