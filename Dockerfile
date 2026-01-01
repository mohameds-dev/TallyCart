FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install psycopg2 for PostgreSQL
RUN pip install --no-cache-dir psycopg2-binary

# Copy project code
COPY server/ /app/server/
COPY pyrightconfig.json /app/

# Copy entrypoint scripts
COPY container_scripts/docker-entrypoint.sh /app/docker-entrypoint.sh
COPY container_scripts/docker-entrypoint-celery.sh /app/docker-entrypoint-celery.sh
RUN chmod +x /app/docker-entrypoint.sh /app/docker-entrypoint-celery.sh

WORKDIR /app/server

# Expose port
EXPOSE 8000

