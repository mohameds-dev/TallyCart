# TallyCart

A backend service for tracking product prices and building optimized shopping lists to make grocery shopping cheaper and easier. The system ingests receipt data (via scan or upload), parses it through OCR and LLM-based extraction, and exposes structured product and shop data via a REST API.

---

## Highlights

- **Test-driven development** — Test suite enforces a **minimum 90% code coverage**; CI/CD fails if coverage drops below that threshold.
- **Fully dockerized** — Single `docker-compose up` brings up Django, Celery, PostgreSQL, and Redis with health checks and automatic migrations.
- **Receipt processing pipeline** — End-to-end flow: upload image → OCR (EasyOCR) → LLM parsing (Gemini) → structured JSON; async via Celery and status polling.
- **REST API** — Products (with price snapshots and tags), shops (with search), and receipts (scan, list, detail) are available and tested.

---

## Tech Stack

| Layer        | Technology                    |
|-------------|-------------------------------|
| Backend     | Django 4.2, Django REST Framework |
| Task queue  | Celery, Redis                 |
| Database    | PostgreSQL 15                 |
| OCR         | EasyOCR, OpenCV (headless)    |
| LLM         | Google Gemini API             |
| Containers  | Docker, Docker Compose        |
| CI/CD       | GitHub Actions (tests + coverage gate) |

---

## What’s in place

- **Products API** — CRUD, price snapshots, tags, search by name/tag.
- **Shops API** — CRUD, search by name and address.
- **Receipts API** — `POST /receipts/scan/` with an image → returns scan ID; `GET /receipts/<id>/` for status and parsed receipt data. Processing runs asynchronously in Celery.
- **Receipt pipeline** — Image preprocessing (OpenCV), OCR (EasyOCR), structured extraction and revision (Gemini), stored as JSON with accuracy evaluation utilities.
- **Test suite** — Unit and integration tests for views, tasks, parsers, and utilities; mocks used for OCR/LLM so tests are fast and deterministic.

---

## Current focus

The project is in active development. Current priorities:

1. **Data and content** — Loading and curating more product/shop data.
2. **User auth** — Designing and implementing the user model and authentication for the API.
3. **API expansion** — Additional endpoints and features to support the future frontend.
4. **Frontend** — Planned after the API and auth are in a good place.

---

## Getting started

### Prerequisites

- Docker and Docker Compose
- For receipt scanning: a [Gemini API key](https://aistudio.google.com/app/apikey) (optional for running the app; required for the scan pipeline)

### Run with Docker

1. Clone the repo and add a `.env` file in the project root (see [Environment variables](#environment-variables)).

2. Build and start all services:

   ```bash
   docker-compose up --build
   ```

3. Use the app:

   - **Django API:** http://localhost:8000  
   - **Products:** http://localhost:8000/products/  
   - **Shops:** http://localhost:8000/shops/  
   - **Receipts (list):** http://localhost:8000/receipts/  
   - **Scan receipt:** `POST http://localhost:8000/receipts/scan/` with `image` (multipart file)

The entrypoint scripts wait for PostgreSQL, run migrations, then start the server and Celery worker.

### Services

| Service  | Description                                      |
|----------|--------------------------------------------------|
| `server` | Django app (runserver; code reload via volume)   |
| `celery` | Celery worker for receipt processing             |
| `db`     | PostgreSQL 15 (data in `postgres_data` volume)   |
| `redis`  | Redis (Celery broker)                            |

---

## Environment variables

Containers use the root `.env` file (via `env_file` and `environment` in `docker-compose.yml`). Recommended variables:

| Variable           | Description                                      |
|--------------------|--------------------------------------------------|
| `DJANGO_SECRET_KEY`| Secret for Django (required in production)       |
| `GEMINI_API_KEY`   | Google AI Studio key for receipt LLM parsing     |
| `DEBUG`            | Set to `True` for local development              |
| `REDIS_URL`        | Override if not using default Redis in Compose   |

See `.env.example` for a template. The `.env` file is gitignored.

---

## Running tests locally

From the project root, with a virtualenv that has dependencies installed:

```bash
cd server
python manage.py test
```

With coverage (must meet 90% to pass in CI):

```bash
cd server
coverage run --source='.' manage.py test
coverage report --fail-under=90
```

---

## Project board

Roadmap and tasks: [GitHub Project Board](https://github.com/users/mohameds-dev/projects/3).
