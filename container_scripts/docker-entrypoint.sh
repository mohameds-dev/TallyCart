#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
# Using defaults that match docker-compose.yml
echo "Waiting for PostgreSQL..."
until pg_isready -h db -U tallycart -d tallycart; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing command"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Execute the main command
exec "$@"

