import logging
from app.rag.ingestion.loader import DocumentLoader
from app.rag.operations.vector_store import VectorStoreOperations

logger = logging.getLogger(__name__)


class IngestionOperations:
    async def ingest_content(self, content: str, user_id: str) -> dict:
        try:
            documents = DocumentLoader().load_document_from_content(content, user_id)
            VectorStoreOperations(user_id).add_documents(documents)
            return {
                "document_count": len(documents)
            }
        except Exception as e:
            logger.error(f"Error ingesting content: {str(e)}")
            raise
