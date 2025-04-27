from langchain_openai import ChatOpenAI
from app.agent.enum import RetrievalGradeType, AgentStateType
from langchain_core.messages import SystemMessage
import logging
from langchain_core.prompts import PromptTemplate
from app.config.settings import OPENAI_MODEL
from app.utils.logger import PrettyLogger

logger = logging.getLogger(__name__)
pretty_logger = PrettyLogger(logger)


def retrieval_transition(state: AgentStateType):
    model = ChatOpenAI(temperature=0.8, model=OPENAI_MODEL)
    llm_with_tool = model.with_structured_output(RetrievalGradeType)

    chain = PromptTemplate(
        template="""
            You are a relevance assessment assistant. Your job is to determine if the retrieved
            document contains information that is relevant to answering the user's question.

            Retrieved document:
            ----------------
            {context}
            ----------------

            User's question:
            ----------------
            {question}
            ----------------

            Determine if the document contains relevant information that helps answer the user's question.

            If the document contains information that directly addresses the question or provides helpful context, respond with "yes".
            If the document is unrelated or does not provide useful information for the question, respond with "no".

            Your response must be exactly "yes" or "no" with no additional text.
        """,
        input_variables=["context", "question"],
    ) | llm_with_tool

    question = state.query

    last_system_message = next(
        (msg for msg in reversed(state.messages) if isinstance(msg, SystemMessage)), None
    )
    if not last_system_message:
        pretty_logger.info("Edge: No system message found, ending")
        return "end"

    context = last_system_message.content

    if context == "No relevant documents found for user":
        pretty_logger.info("Edge: No relevant documents found, routing to fallback")
        return "end"

    scored_result = chain.invoke({"question": question, "context": context})
    pretty_logger.info(f"Edge: Scored result: {scored_result}")
    if scored_result.binary_score == "yes":  # type: ignore
        pretty_logger.info("Edge: Document is relevant, routing to response")
        return "response"
    else:
        pretty_logger.info("Edge: Document is not relevant, ending")
        return "end"
