import time
import psycopg
import asyncio
import logging

logger = logging.getLogger(__name__)


def get_psycopg_connection():
    from app.config.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    conn_string = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"
    try:
        conn = psycopg.connect(conn_string)
        conn.autocommit = True
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def wait_for_database(max_retries: int = 10, retry_interval: int = 5) -> bool:
    for attempt in range(max_retries):
        try:
            conn = get_psycopg_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                conn.close()
                logger.info(f"Database connection established after {attempt} attempts")
                return True
        except Exception as e:
            logger.warning(f"Database connection attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)

    logger.error(f"Failed to connect to database after {max_retries} attempts")
    return False


def clear_tables() -> bool:
    conn = get_psycopg_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE langchain_pg_embedding CASCADE;")
            cursor.execute("TRUNCATE TABLE langchain_pg_collection CASCADE;")
            logger.info("All tables cleared successfully")
            return True
    except Exception as e:
        logger.error(f"Error clearing tables: {e}")
        return False
    finally:
        conn.close()


def setup_database_schema() -> bool:
    conn = get_psycopg_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS langchain_pg_collection (
                    uuid UUID PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL,
                    cmetadata JSONB
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS langchain_pg_embedding (
                    id VARCHAR,
                    collection_id UUID REFERENCES langchain_pg_collection(uuid) ON DELETE CASCADE,
                    embedding VECTOR(1536),
                    document TEXT,
                    cmetadata JSONB,
                    custom_id TEXT,
                    PRIMARY KEY (id)
                );
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS langchain_pg_embedding_metadata_idx
                ON langchain_pg_embedding USING GIN (cmetadata);
            """)

            logger.info("Database schema setup complete")
            return True
    except Exception as e:
        logger.error(f"Error setting up database schema: {e}")
        return False
    finally:
        conn.close()


async def restart_database() -> bool:
    if not wait_for_database():
        logger.error("Could not connect to the database")
        return False

    if not clear_tables():
        logger.error("Failed to clear tables")
        return False

    if not setup_database_schema():
        logger.error("Failed to setup database schema")
        return False

    return True


def run_restart():
    return asyncio.run(restart_database())


if __name__ == "__main__":
    run_restart()
