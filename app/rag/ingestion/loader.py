from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)


class DocumentLoader:
    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_document_from_content(self, content: str, user_id: str) -> List[Document]:
        try:
            doc = Document(page_content=content)
            splits = self.text_splitter.split_documents([doc])
            return splits
        except Exception as e:
            logger.error(f"Error loading document: {str(e)}")
            raise
