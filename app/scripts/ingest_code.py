#!/usr/bin/env python
import asyncio
import argparse
import sys
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from app.rag.ingest import ingest_folder

class TerminalColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

logging.basicConfig(
    level=logging.INFO,
    format=f'{TerminalColors.BOLD}%(asctime)s{TerminalColors.ENDC} - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

async def run_ingest(folder_path, user_id, extension):
    print(f"\n{TerminalColors.BLUE}🔍 Ingesting code for User: {user_id}{TerminalColors.ENDC}")
    print(f"{TerminalColors.BLUE}📂 Folder: {folder_path}{TerminalColors.ENDC}")
    print(f"{TerminalColors.BLUE}🔖 Extension: {extension}{TerminalColors.ENDC}\n")

    result = await ingest_folder(folder_path, user_id, extension)

    if result:
        print(f"\n{TerminalColors.GREEN}✅ Successfully ingested {result['count']} files!{TerminalColors.ENDC}")
        for i, file in enumerate(result['files'][:5]):
            print(f"{TerminalColors.GREEN}   → {file}{TerminalColors.ENDC}")

        if len(result['files']) > 5:
            print(f"{TerminalColors.GREEN}   → ... and {len(result['files']) - 5} more files{TerminalColors.ENDC}")
    else:
        print(f"\n{TerminalColors.RED}❌ Ingestion failed.{TerminalColors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description="Ingest code files from a folder")
    parser.add_argument("folder_path", help="Path to the folder containing code files")
    parser.add_argument("user_id", help="User ID to associate with the ingested files")
    parser.add_argument("extension", nargs='?', default=".py", help="File extension to filter by (default: .py)")

    args = parser.parse_args()

    try:
        asyncio.run(run_ingest(args.folder_path, args.user_id, args.extension))
    except KeyboardInterrupt:
        print(f"\n{TerminalColors.YELLOW}Ingestion interrupted.{TerminalColors.ENDC}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"\n{TerminalColors.RED}❌ Error: {str(e)}{TerminalColors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()