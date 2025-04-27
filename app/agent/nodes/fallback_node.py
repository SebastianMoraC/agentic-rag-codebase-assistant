from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.agent.enum import AgentStateType
from app.config.settings import OPENAI_MODEL
import logging
from app.utils.logger import PrettyLogger

logger = logging.getLogger(__name__)
pretty_logger = PrettyLogger(logger)


class FallbackNode:
    def __call__(self, state: AgentStateType) -> AgentStateType:
        pretty_logger.info("Node: Generating concise fallback response")
        messages = state.messages
        question = state.query
        last_system_message = messages[-1]

        context = "No context available" if not last_system_message else last_system_message.content

        prompt = f"""
        You are a senior developer replying in a confident, chat-like tone.

        USER QUESTION:
        {question}

        CONTEXT FOUND IN CODEBASE (NOT USEFUL):
        {context}

        RESPONSE INSTRUCTIONS:
        1. Let the user know, clearly and confidently, that their question doesn’t apply to the codebase or project.
        2. Do **not** try to answer the question itself if it’s not related.
        3. Be short and direct. Say that the question is not related with the context of this codebase, if you can do it try to explain why.
        4. Do **not** mention context, RAG, or documents used.
        5. Use friendly but no-nonsense language — like you're talking to a teammate.
        6. Respond in the user’s language (default: SPANISH).
        7. No filler or unnecessary explanations. Just state that the question is out of scope for this code.
        """

        llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.4, streaming=False)
        fallback_chain = llm | StrOutputParser()
        fallback_response = fallback_chain.invoke(prompt)

        state.messages.append(AIMessage(content=fallback_response))
        state.user_response = fallback_response

        return state
