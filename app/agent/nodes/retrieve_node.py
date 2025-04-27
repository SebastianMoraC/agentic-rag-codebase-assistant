from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from app.config.settings import EMBEDDING_MODEL, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app.agent.enum import AgentStateType
from langchain_core.messages import SystemMessage
import logging
from app.utils.logger import PrettyLogger

logger = logging.getLogger(__name__)
pretty_logger = PrettyLogger(logger)


class RetrieveNode:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        self.conn_str = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    def __call__(self, state: AgentStateType) -> AgentStateType:
        pretty_logger.info(f"Starting retrieval for user: {state.user_id}")
        collection_name = f'{state.user_id}_collection'
        vector_store = PGVector(
            collection_name=collection_name,
            connection=self.conn_str,
            embeddings=self.embeddings,
            use_jsonb=True
        )

        try:
            docs = vector_store.similarity_search_with_score(
                state.query,
                k=5
            )

            if docs:
                context = "\n\n---\n\n".join([doc.page_content for doc, _ in docs])
                pretty_logger.info(f"Context Retrieved: {context[:100]}...")
                state.messages.append(SystemMessage(content=f"{context}"))
            else:
                pretty_logger.info("Node: No relevant documents found")
                state.messages.append(SystemMessage(content="No relevant documents found for user"))

        except Exception as e:
            pretty_logger.error(f"Node: Error during retrieval - {str(e)}")
            state.messages.append(SystemMessage(content="I encountered an error while trying to answer your question."))

        return state
