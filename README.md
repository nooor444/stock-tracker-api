# Stock Tracker API

A production-grade REST API for real-time stock data — built with FastAPI and deployed on AWS.

## Architecture

```
EventBridge (hourly)
      │
      ▼
  AWS Lambda          ← triggers ingestion
      │
      ▼
  AWS EC2             ← FastAPI application server
      │
      ├── SQLite DB   ← local query layer
      │
      └── AWS S3      ← persistent database backups
```

**Stack:** Python · FastAPI · SQLite · AWS EC2 · AWS S3 · AWS Lambda · Plotly

---

## Live API

Base URL: `http://54.77.164.94:8000`

| Endpoint | Method | Description |
|---|---|---|
| `/docs` | GET | Interactive Swagger UI |
| `/ingest` | POST | Fetch and store latest stock prices |
| `/stocks/{ticker}` | GET | Full price history for a ticker |
| `/stocks/{ticker}/latest` | GET | Most recent price entry |
| `/analytics/{ticker}` | GET | Trend summary and price movement |
| `/visualise/{ticker}` | GET | Plotly time-series chart |

---

## Key Features

- **Cloud-native deployment** on AWS EC2 (t2.micro, Ubuntu 22.04)
- **Persistent storage** — SQLite DB backed up to S3 on every write
- **Automated ingestion** — AWS Lambda triggered hourly via EventBridge
- **Analytics endpoints** — price trends, moving averages, percentage changes
- **Interactive visualisations** — Plotly time-series charts served directly from the API
- **Clean API design** — input validation, error handling, modular service structure

---

## Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/stock-tracker-api
cd stock-tracker-api
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API docs.

---

## AWS Deployment

The API is deployed on AWS using three services:

**EC2** — application server running FastAPI via Gunicorn  
**S3** — bucket for SQLite database backups (`stock-tracker-data/backups/`)  
**Lambda** — scheduled function that hits `/ingest` every hour via EventBridge

See [`/docs/aws-setup.md`](docs/aws-setup.md) for full deployment steps.

---

## Project Structure

```
stock-tracker-api/
├── main.py              # FastAPI app + route definitions
├── database.py          # SQLite connection + schema
├── ingestion.py         # Stock data fetching logic
├── analytics.py         # Trend analysis functions
├── s3_backup.py         # S3 upload utility
├── requirements.txt
└── docs/
    └── aws-setup.md     # AWS deployment guide
```

---

## Skills Demonstrated

`REST API design` `microservices` `cloud-native deployment` `AWS` `distributed systems`  
`Python` `FastAPI` `SQL` `data ingestion` `CI/CD` `operational monitoring`
