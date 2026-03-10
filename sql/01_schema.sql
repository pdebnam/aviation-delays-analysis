-- ===========================================
-- Schema: Core fact table
-- Source: BTS On-Time Performance (processed)
--============================================

DROP TABLE IF EXISTS fact_flights;

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
)