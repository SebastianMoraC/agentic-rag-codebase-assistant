#!/usr/bin/env python
from app.agent.enum import AgentStateType
from app.agent.agent import Agent
import asyncio
import argparse
import sys
from pathlib import Path
import logging
import signal
from typing import Any
from app.utils.logger import PrettyLogger, TerminalColors

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


logging.basicConfig(
    level=logging.INFO,
    format='{}{}{} - %(levelname)s - %(message)s'.format(
        TerminalColors.BLUE, '%(asctime)s', TerminalColors.ENDC
    ),
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)
pretty_logger = PrettyLogger(logger)


def extract_response_from_result(result):
    if isinstance(result, AgentStateType) and hasattr(result, 'messages') and result.messages:
        last_message = result.messages[-1]
        if hasattr(last_message, 'content'):
            return str(last_message.content)

    if isinstance(result, dict):
        if 'messages' in result and result['messages'] and len(result['messages']) > 0:
            last_message = result['messages'][-1]
            if isinstance(last_message, dict) and 'content' in last_message:
                return str(last_message['content'])

        if 'response' in result:
            return str(result['response'])

    if hasattr(result, 'content'):
        content = getattr(result, 'content')
        if isinstance(content, str):
            return content

    return ""


async def process_query(query, user_id):
    try:
        agent = Agent()

        state = AgentStateType(
            user_id=user_id,
            query=query
        )

        pretty_logger.info("Invoking agent...")
        result: dict[str, Any] = agent.compiled_graph.invoke(state)
        pretty_logger.info("Agent execution completed")
        response_text: str = result.get("user_response", "")

        if response_text:
            print(f"\n{TerminalColors.GREEN}🤖 Response:{TerminalColors.ENDC}")
            print(f"{TerminalColors.YELLOW}{response_text}{TerminalColors.ENDC}\n")
        else:
            print(f"\n{TerminalColors.YELLOW}⚠️ No response generated.{TerminalColors.ENDC}\n")

    except Exception as e:
        pretty_logger.error(f"Error processing query: {str(e)}")
        print(f"\n{TerminalColors.RED}❌ Error: {str(e)}{TerminalColors.ENDC}\n")


async def query_loop(user_id):
    print(f"\n{TerminalColors.BLUE}🧠 Private Codebase Agent{TerminalColors.ENDC}")
    print(f"{TerminalColors.BLUE}👤 User: {user_id}{TerminalColors.ENDC}")
    print(f"{TerminalColors.YELLOW}Type your questions about the codebase. Press Ctrl+C to exit.{TerminalColors.ENDC}\n")

    while True:
        try:
            query = input(f"{TerminalColors.BOLD}Ask: {TerminalColors.ENDC}")

            if not query.strip():
                continue

            print(f"{TerminalColors.BLUE}🔍 Processing: {query}{TerminalColors.ENDC}")
            await process_query(query, user_id)

        except KeyboardInterrupt:
            print(f"\n{TerminalColors.YELLOW}Exiting...{TerminalColors.ENDC}")
            break
        except EOFError:
            print(f"\n{TerminalColors.YELLOW}Exiting...{TerminalColors.ENDC}")
            break


def signal_handler(sig, frame):
    print(f"\n{TerminalColors.YELLOW}Exiting...{TerminalColors.ENDC}")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Query your codebase with natural language")
    parser.add_argument("user_id", help="Your user ID")

    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        asyncio.run(query_loop(args.user_id))
    except Exception as e:
        pretty_logger.error(f"Error: {str(e)}")
        print(f"\n{TerminalColors.RED}❌ Error: {str(e)}{TerminalColors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
