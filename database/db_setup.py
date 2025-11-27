import os
import sys
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# Load .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Locate results_data_* folders
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
csv_folders = [f for f in os.listdir(root_dir)
               if f.startswith("results_data_") and os.path.isdir(os.path.join(root_dir, f))]

if not csv_folders:
    print("❌ There is no results_data_* folder.")
    sys.exit(0)

# Collect CSVs
csv_paths = []
for folder in csv_folders:
    p = os.path.join(root_dir, folder, "output_data_with_category.csv")
    if os.path.exists(p):
        csv_paths.append(p)

if not csv_paths:
    print("❌ CSV file not found in any results_data_* folder.")
    sys.exit(0)

print(f"✅ Found {len(csv_paths)} CSV file(s).")

# Read & normalize
try:
    df_list = [pd.read_csv(p) for p in csv_paths]
    df = pd.concat(df_list, ignore_index=True)
    df.rename(columns={
        "date": "scraped_at",
        "link": "site",
        "kubikmeter": "volume",
        "produkt": "product"
    }, inplace=True)
    df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")
    df = df.dropna(subset=["scraped_at"])
    print(f"✅ Total rows before filtering: {len(df)}")
except Exception as e:
    print("❌ Failed to read or process CSVs:", e)
    sys.exit(1)

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = False
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL.")
except Exception as e:
    print("❌ Error connecting to the database:", e)
    sys.exit(1)

# Create table (no generated column for migration-safety)
create_table_sql = """
CREATE TABLE IF NOT EXISTS scraped_data (
    id SERIAL PRIMARY KEY,
    scraped_at TIMESTAMP,
    site TEXT,
    volume DOUBLE PRECISION,
    product TEXT,
    currency TEXT,
    price DOUBLE PRECISION,
    type TEXT,
    category TEXT,
    subcategory TEXT
);
"""

# Ensure scraped_date column exists (plain DATE)
add_scraped_date_sql = """
ALTER TABLE scraped_data
ADD COLUMN IF NOT EXISTS scraped_date DATE;
"""

# Backfill scraped_date for existing rows
backfill_scraped_date_sql = """
UPDATE scraped_data
SET scraped_date = scraped_at::date
WHERE scraped_date IS NULL AND scraped_at IS NOT NULL;
"""

# Unique index by day/site/volume/product
create_unique_idx_sql = """
CREATE UNIQUE INDEX IF NOT EXISTS unique_entry_per_day
ON scraped_data (scraped_date, site, volume, product);
"""

try:
    cursor.execute(create_table_sql)
    cursor.execute(add_scraped_date_sql)
    cursor.execute(backfill_scraped_date_sql)
    cursor.execute(create_unique_idx_sql)
    conn.commit()
    print("✅ Table, column scraped_date, and unique index ensured.")
except Exception as e:
    conn.rollback()
    print("❌ Failed to create/alter table or index:", e)
    cursor.close()
    conn.close()
    sys.exit(1)

# Determine current day from data
current_day = df["scraped_at"].dt.date.max()
if pd.isna(current_day):
    print("❌ Error: No valid date found in scraped_at column.")
    cursor.close()
    conn.close()
    sys.exit(0)

# Clean existing rows for that day
try:
    cursor.execute("DELETE FROM scraped_data WHERE scraped_date = %s;", (current_day,))
    conn.commit()
    print(f"✅ Deleted existing data for date: {current_day}")
except Exception as e:
    conn.rollback()
    print("❌ Failed to delete old data for current day:", e)
    cursor.close()
    conn.close()
    sys.exit(1)

# Insert rows (including scraped_date)
insert_sql = """
INSERT INTO scraped_data (
    scraped_at, scraped_date, site, volume, product, currency, price, type, category, subcategory
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

try:
    for _, row in df.iterrows():
        scraped_at = pd.to_datetime(row["scraped_at"]) if pd.notna(row["scraped_at"]) else None
        scraped_date = scraped_at.date() if scraped_at else None

        cursor.execute(insert_sql, (
            scraped_at,
            scraped_date,
            row.get("site"),
            float(row["volume"]) if pd.notna(row.get("volume")) else None,
            row.get("product"),
            row.get("currency"),
            float(row["price"]) if pd.notna(row.get("price")) else None,
            row.get("type"),
            row.get("category"),
            row.get("subcategory"),
        ))
    conn.commit()
    print("✅ Data inserted successfully (duplicates skipped by constraint).")
except Exception as e:
    conn.rollback()
    print("❌ Failed to insert data:", e)
finally:
    cursor.close()
    conn.close()
