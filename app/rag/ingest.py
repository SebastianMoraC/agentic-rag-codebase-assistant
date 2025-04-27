from pathlib import Path
import logging

from app.rag.operations.ingestion import IngestionOperations

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def ingest_folder(folder_path: str, user_id: str, extension: str = ".py"):
    folder = Path(folder_path)
    if not folder.exists():
        logger.error(f"Folder not found: {folder_path}")
        return

    ingestion_ops = IngestionOperations()
    ingested_count = 0
    processed_files = []

    logger.info(f"🔍 Starting ingestion process for user {user_id}...")
    logger.info(f"📁 Looking for *{extension} files in {folder_path}")

    for file_path in folder.glob(f"**/*{extension}"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            result = await ingestion_ops.ingest_content(content, user_id)
            ingested_count += 1
            processed_files.append(file_path.relative_to(folder))

            logger.info(f"✅ Processed: {file_path.relative_to(folder)} ({result.get('document_count', 0)} chunks)")

        except Exception as e:
            logger.error(f"❌ Error processing file {file_path}: {str(e)}")

    logger.info(f"🎉 Finished ingestion! Processed {ingested_count} files for user {user_id}")
    return {
        "count": ingested_count,
        "files": processed_files
    }
