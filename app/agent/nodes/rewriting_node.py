from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.agent.enum import AgentStateType
from app.config.settings import OPENAI_MODEL
import logging
from app.utils.logger import PrettyLogger

logger = logging.getLogger(__name__)
pretty_logger = PrettyLogger(logger)


class RewritingNode:
    def __call__(self, state: AgentStateType) -> AgentStateType:
        pretty_logger.info("Node: Rewriting query for better retrieval")
        original_query = state.query

        prompt = f"""
        You are an expert at reformulating search queries to get precise code retrieval results.

        ORIGINAL QUERY:
        {original_query}

        TASK:
        Transform this query into a specific, technical search format that will improve code retrieval.
        Include relevant programming concepts, function names, or technical terms implied in the query.
        Focus on extracting technical intent rather than adding new requirements.
        Be concise and use standard programming terminology.
        Never ask for clarification or additional information.
        """

        llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.7)
        rewriting_chain = llm | StrOutputParser()
        rewritten_query = rewriting_chain.invoke(prompt)

        state.query = rewritten_query
        state.retrieval_retry_count += 1

        state.messages.append(SystemMessage(content=f"Rewritten query: {rewritten_query}"))

        return state
