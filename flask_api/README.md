# Flask API Service

This Flask application exposes the `scraped_data` table from PostgreSQL as a REST API.  
Authentication is required for all endpoints, and credentials are configured in the `.env` file.

---

## 🔹 Features
- Connects to PostgreSQL using settings from `database/.env`.
- Provides authenticated API endpoints.
- Returns data in JSON format.
- Supports filtering by site.

---

## 🔹 Requirements
- Python 3.x  
- PostgreSQL running and accessible  
- Dependencies:
  - `Flask`
  - `Flask-SQLAlchemy`
  - `Flask-HTTPAuth`
  - `psycopg2`
  - `python-dotenv`

Install dependencies:
```bash
pip install flask flask-sqlalchemy flask-httpauth psycopg2 python-dotenv
