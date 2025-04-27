from typing import List
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from app.config.settings import EMBEDDING_MODEL, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import logging

logger = logging.getLogger(__name__)


class VectorStoreOperations:
    def __init__(self, user_id: str):
        self.collection_name = f"{user_id}_collection"
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        self.conn_str = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    def get_vector_store(self) -> PGVector:
        return PGVector(
            collection_name=self.collection_name,
            connection=self.conn_str,
            embeddings=self.embeddings,
            use_jsonb=True
        )

    def add_documents(self, documents: List[Document]) -> None:
        try:
            vector_store = self.get_vector_store()
            vector_store.add_documents(
                documents=documents,
            )
            logger.info(f"Successfully added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
