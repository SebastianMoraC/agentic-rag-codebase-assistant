from app.agent.enum import AgentStateType, ResponseEvaluationType
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.config.settings import OPENAI_MODEL
import logging
from app.utils.logger import PrettyLogger

logger = logging.getLogger(__name__)
pretty_logger = PrettyLogger(logger)


def response_transition(state: AgentStateType):
    pretty_logger.info("Edge: Evaluating response and deciding next step")

    user_query = state.query
    response_message = state.user_response

    if state.retrieval_retry_count == 0:
        pretty_logger.info("Edge: Already retried retrieval twice, ending flow")
        return "end"

    model = ChatOpenAI(temperature=0.2, model=OPENAI_MODEL)
    llm_with_tool = model.with_structured_output(ResponseEvaluationType)

    chain = PromptTemplate(
        template="""
        You are evaluating if a given response properly addresses the user's query.

        USER QUERY:
        {question}

        RESPONSE GENERATED:
        {response}

        Determine if the response directly addresses the user's question based on the context.
        If the response is not relevant or incomplete, decide if we should try to rewrite the query.

        EVALUATION CRITERIA:
        - is_relevant: Set to true if the response addresses the user query
        - needs_rewriting: Set to true if the response is not relevant and we should retry with a rewritten query
        """,
        input_variables=["question", "response"],
    ) | llm_with_tool
    pretty_logger.info(f"Edge: User query: {user_query}")
    pretty_logger.info(f"Edge: Response summary: {response_message[:50]}...")
    evaluation = chain.invoke({
        "question": user_query,
        "response": response_message
    })

    state.messages.append(SystemMessage(content=f"EVALUATION: {evaluation}"))
    pretty_logger.info(f"Edge: Evaluation result: {evaluation}")
    if evaluation.is_relevant:  # type: ignore
        pretty_logger.info("Edge: Response is relevant, ending flow")
        return "end"
    elif evaluation.needs_rewriting:  # type: ignore
        pretty_logger.info("Edge: Response needs rewriting, routing to rewriting node")
        return "rewriting"
    else:
        pretty_logger.info("Edge: Response insufficient, routing to fallback node")
        return "fallback"
