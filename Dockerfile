# Use a specific hash or just stick to slim for speed
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps: postgresql-client for DB, libgomp1 for PyTorch/EasyOCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libgomp1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt psycopg2-binary

COPY container_scripts/docker-entrypoint.sh /app/docker-entrypoint.sh
COPY container_scripts/docker-entrypoint-celery.sh /app/docker-entrypoint-celery.sh
RUN chmod +x /app/docker-entrypoint.sh /app/docker-entrypoint-celery.sh

COPY server/ /app/server/
COPY pyrightconfig.json /app/

WORKDIR /app/server

EXPOSE 8000