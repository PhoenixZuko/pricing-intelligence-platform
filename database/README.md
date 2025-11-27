# CSV Importer to PostgreSQL

This script automates the process of importing scraped data (from CSV files) into a PostgreSQL database.  
It ensures that data is normalized, avoids duplicates, and keeps the database always updated with the latest results.

---

## 🔹 Features
- Loads database connection variables from `.env`.
- Scans all `results_data_*` folders for CSV files named `output_data_with_category.csv`.
- Reads and merges CSV files into one dataset.
- Normalizes column names (`date → scraped_at`, `link → site`, etc.).
- Creates the `scraped_data` table if it does not exist.
- Ensures uniqueness per day, site, volume, and product (via unique index).
- Deletes existing records for the current day before inserting new ones.
- Inserts new rows into PostgreSQL (skips duplicates automatically).

---

## 🔹 Requirements
- Python 3.x  
- PostgreSQL running and accessible  
- Dependencies:
  - `psycopg2`
  - `pandas`
  - `python-dotenv`

Install dependencies:
```bash
pip install psycopg2 pandas python-dotenv
