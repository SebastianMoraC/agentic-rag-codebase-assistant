# Agentic RAG Codebase Assistant

A Retrieval-Augmented Generation (RAG) system that helps you query your codebase using natural language. This agent will ingest your code files, store them in a vector database, and allow you to ask questions about your code.

## 🚀 Features

- Code file ingestion with customizable file extensions
- Vector-based code retrieval using pgvector
- Natural language querying of your codebase
- Docker and DevContainer support for easy setup

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized setup)
- PostgreSQL with pgvector extension (handled by Docker setup)
- OpenAI API key

## 🔧 Environment Setup

1. Clone the `.devcontainer` from the example:

```bash
cp -r .devcontainer_example .devcontainer
```

2. Create a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vectordb
```

3. Create a Docker network (if not already created):

```bash
docker network create rag-network
```

## 🐳 Docker Setup

1. Build and start the Docker containers:

```bash
docker-compose -f docker/docker-compose.yml up -d
```

2. Setup the database:

```bash
docker exec -it knowledge_code_vscode python -m app.db.setup
```

## 🔨 Local Setup (without Docker)

1. Install the required packages:

```bash
pip install -r requirements/base.txt
pip install langchain-postgres==0.0.13 psycopg pgvector
```

2. Ensure PostgreSQL with pgvector extension is installed and running

3. Setup the database:

```bash
python -m app.db.setup
```

## 📈 Usage

### 1. Initialize the Database

Before using the system, make sure to initialize the database:

```bash
python -m app.db.setup
```

This command will:
- Connect to the PostgreSQL database
- Create the necessary tables and indexes
- Set up the vector extension

### 2. Ingest Code

To ingest code from a directory:

```bash
python ingest.py /path/to/your/code user_id [file_extension]
```

Parameters:
- `/path/to/your/code`: Path to the directory containing code files
- `user_id`: Identifier for the user (used to organize ingested content)
- `file_extension`: Optional file extension filter (default: `.py`)

Example:

```bash
python ingest.py ./src my_project .js
```

### 3. Query Your Codebase

To ask questions about your codebase:

```bash
python query.py user_id
```

Parameters:
- `user_id`: The same user ID used during ingestion

This will start an interactive query session where you can ask questions about your codebase.

Example:

```bash
python query.py my_project
```

## 🏗️ Project Structure

- `app/`: Main application code
  - `agent/`: Agent implementation for processing queries
  - `db/`: Database interactions and setup
  - `rag/`: Retrieval-augmented generation components
  - `scripts/`: Command-line scripts for ingestion and querying
  - `utils/`: Utility functions and helpers
- `docker/`: Docker configuration
- `requirements/`: Python dependencies

## 🔍 Advanced Usage

### Using DevContainer in VS Code

This project includes a DevContainer configuration for VS Code. To use it:

1. Install the "Remote - Containers" extension in VS Code
2. Clone the `.devcontainer_example` to `.devcontainer`
3. Open the project in VS Code and click "Reopen in Container" when prompted

### Customizing Vector Search

You can adjust the relevance threshold in `config.py` to control the strictness of vector similarity matches.

## 🛠️ Troubleshooting

- If you encounter database connection issues, ensure PostgreSQL is running and accessible
- For ingestion problems, check file permissions and path correctness
- If queries return no results, try ingesting more code files or adjusting the relevance threshold
