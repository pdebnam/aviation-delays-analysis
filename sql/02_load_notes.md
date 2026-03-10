# Data Load Notes

This document describes how the processed flight delay dataset is loaded into the SQLite database used for analysis in this project.

The goal of this step is to create a clean, reproducible SQL environment that mirrors the exploratory analysis performed in Python.

---

## Source Data

- Dataset: U.S. Bureau of Transportation Statistics (BTS) – Reporting Carrier On-Time Performance
- Scope: Domestic flights, October 2025
- File used for SQL load:
  - `data/processed/flights_oct_2025_processed.csv`

This CSV is the output of the Python data cleaning and EDA phase and represents a validated, analysis-ready dataset.

---

## Load Method

The data is loaded into SQLite using a Python script:

- Script location: `python/load_to_sqlite.py`
- Database file created: `data/flights.db`

SQLite is used as a lightweight, file-based database suitable for local analytics and portfolio work. No external database server is required.

---

## Load Steps (High Level)

1. Read the processed CSV into a pandas DataFrame
2. Rename columns to SQL-friendly snake_case
3. Create (or recreate) the `fact_flights` table
4. Insert all rows from the DataFrame into the table
5. Commit and close the database connection

This process is repeatable and can be rerun at any time to recreate the database from scratch.

---

## Table Created

### fact_flights

This is the primary fact table used for all analysis and visualization.

Columns include:

- fl_date
- year
- month
- day_of_week
- op_unique_carrier
- origin
- dest
- distance
- dep_delay
- arr_delay_clean
- is_delayed

Each row represents a single completed flight.

---

## Important Assumptions

- Only completed (non-canceled, non-diverted) flights are included
- A flight is considered delayed if arrival delay ≥ 15 minutes
