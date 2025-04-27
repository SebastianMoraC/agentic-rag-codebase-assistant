FROM python:3.11-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  git \
  libssl-dev swig python3-dev gcc \
  libpq-dev


WORKDIR /app
COPY requirements /requirements
RUN pip install -r /requirements/base.txt \
    && pip install langchain-postgres==0.0.13 psycopg pgvector

EXPOSE 8000

CMD ["sleep", "infinity"]