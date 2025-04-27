from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.agent.enum import AgentStateType
from app.config.settings import OPENAI_MODEL
import logging
from app.utils.logger import PrettyLogger

logger = logging.getLogger(__name__)
pretty_logger = PrettyLogger(logger)


class ResponseNode:
    def __call__(self, state: AgentStateType) -> AgentStateType:
        pretty_logger.info("Node: Generating code-focused response")
        messages = state.messages
        question = state.query
        last_system_message = messages[-1]

        context = last_system_message.content
        prompt = f"""
        You are a senior developer responding in a natural, confident chat tone.

        USER QUESTION:
        {question}

        CODE CONTEXT:
        {context}

        RESPONSE GUIDELINES:
        1. Respond as if you know the answer from experience—no guessing or hedging.
        2. Do **not** mention "the code you’re seeing" or suggest that you're interpreting anything.
        3. Use simple and clear technical language that a junior dev can understand.
        4. Keep it short, precise, and focused on answering the actual question.
        5. Include small code snippets if they help illustrate your point.
        6. If the answer depends on missing details, just say what’s missing—don’t ask the user.
        7. No apologies, no “hope this helps,” no “let me know” — just a direct, helpful answer.
        8. Reply in the user’s language (default: SPANISH).
        9. The tone should feel like a quick, helpful Slack message — clear, human, and to the point.
        """
        llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.7, streaming=False)
        response_chain = llm | StrOutputParser()
        response = response_chain.invoke(prompt)

        state.messages.append(AIMessage(content=response))
        state.user_response = response

        return state
