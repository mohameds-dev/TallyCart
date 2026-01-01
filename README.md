# TallyCart

This is a project for tracking products pricing and help create an optimized shopping cart to make grocery shopping easier and more cost efficient.
View the project's kanban board [here](https://github.com/users/mohameds-dev/projects/3).

### Features under development

- Adding products and shops
- Price tracking
- Product search
- Shopping cart creation & optimization

### Future features:

- Scanning and reading receipts
- Integration with 3rd party API

## Docker Setup

### Prerequisites
- Docker and Docker Compose installed

### Environment Variables

Docker Compose reads environment variables in two ways:

1. **`.env` file in project root** (for Docker Compose variable substitution):
   - Create a `.env` file in the project root (same directory as `docker-compose.yml`)
   - Variables like `${DJANGO_SECRET_KEY}` in docker-compose.yml will be read from this file
   - Example `.env` file:
     ```
     DJANGO_SECRET_KEY=your-secret-key-here
     DEBUG=True
     ```

2. **`env_file` directive** (for container environment variables):
   - The `env_file: - .env` in docker-compose.yml loads variables into containers
   - These are available to Django via `os.getenv()` and `load_dotenv()`
   - Variables in the `environment:` section override `env_file` values

**Note:** The `.env` file is gitignored, so create your own from the example above.

### Running the application

1. Build and start all services:
   ```bash
   docker-compose up --build
   ```

   The entrypoint script will automatically:
   - Wait for PostgreSQL to be ready
   - Run database migrations
   - Start the Django development server

2. Access the application:
   - Django backend: http://localhost:8000
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

### Services
- `server`: Django development server (auto-reloads on code changes)
- `celery`: Celery worker for background tasks
- `db`: PostgreSQL database (data persists in `postgres_data` volume)
- `redis`: Redis for Celery broker

### Notes
- Code changes in `server/` directory will automatically reload without rebuilding
- Database data persists in Docker volume `postgres_data`
- Migrations run automatically on container startup via entrypoint script
- Set `DJANGO_SECRET_KEY` environment variable for production use

