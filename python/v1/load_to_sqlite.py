import pandas as pd
import sqlite3
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "flights_oct_2025_processed.csv"
DB_PATH = PROJECT_ROOT / "data" / "flights.db"

print("CSV path:", CSV_PATH)
print("DB path:", DB_PATH)

# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv(CSV_PATH)

# Rename columns to SQL-friendly names
df = df.rename(columns={
    "FL_DATE": "fl_date",
    "YEAR": "year",
    "MONTH": "month",
    "DAY_OF_WEEK": "day_of_week",
    "OP_UNIQUE_CARRIER": "op_unique_carrier",
    "ORIGIN": "origin",
    "DEST": "dest",
    "DISTANCE": "distance",
    "DEP_DELAY": "dep_delay",
    "ARR_DELAY_CLEAN": "arr_delay_clean",
    "IS_DELAYED": "is_delayed",
})

# -----------------------------
# Create SQLite DB + table
# -----------------------------
conn = sqlite3.connect(DB_PATH)

# Drop table if re-running
conn.execute("DROP TABLE IF EXISTS fact_flights;")

# Create fact table
conn.execute("""
CREATE TABLE fact_flights (
    fl_date TEXT,
    year INTEGER,
    month INTEGER,
    day_of_week INTEGER,
    op_unique_carrier TEXT,
    origin TEXT,
    dest TEXT,
    distance REAL,
    dep_delay REAL,
    arr_delay_clean REAL,
    is_delayed INTEGER
);
""")

# Load data
df.to_sql("fact_flights", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("✅ SQLite database created and loaded successfully")
print(f"✅ Rows loaded: {len(df)}")