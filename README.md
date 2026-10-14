# SupportFlow Ticket Triage API

SupportFlow is a small full-stack practice project that tracks software-support tickets. It was designed around software co-op skills: REST API design, data validation, SQL persistence, automated testing, version control, and containerized execution.

## Features

- Flask REST API with create, read, update, delete, and filter operations
- SQLite database with constraints for priority and status
- Input validation and useful HTTP error responses
- Seven automated pytest tests
- Simple browser dashboard
- Dockerfile for a repeatable local environment

## Run locally

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Run tests

```bash
pytest -q
```

## Run with Docker

```bash
docker build -t supportflow-api .
docker run --rm -p 5000:5000 supportflow-api
```

## API examples

Create a ticket:

```bash
curl -X POST http://127.0.0.1:5000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{"title":"Login fails","description":"The mobile login returns an error.","priority":"high"}'
```

Filter tickets:

```text
GET /api/tickets?status=open&priority=high
```

## How to discuss the project

I built a small ticket-triage service to practice backend software development. I designed REST endpoints, added SQLite constraints and input validation, wrote pytest coverage for normal and error cases, and packaged the service with Docker. The main lesson was separating route handling, validation, persistence, and testing so each part could be debugged independently.
