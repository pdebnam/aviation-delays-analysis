# U.S. Aviation Delays Analysis

## Project Overview

This project analyzes U.S. domestic airline flight data to understand the primary drivers of flight delays and how delay behavior varies across **airlines**, **airports**, and their **interaction**.

Rather than focusing solely on rankings, the goal is to understand *where delay variability originates* and why certain flights experience severe disruptions while most do not.

## Dataset

**Source:** U.S. Bureau of Transportation Statistics (BTS) – Airline On‑Time Performance Data

**Scope:** Domestic U.S. flights (October 2025)



The dataset provides flight‑level records including carrier, origin airport, timing, and arrival delay information. Keeping the scope to one month allowed for deeper exploratory analyst while still working with a large, production-scale dataset (~600k flights).

## Tools

* Python - data cleaning and exploratory data analysis (EDA)
* SQL (SQLite) - data modeling, aggregation, and analytical views
* Git/GitHub - version control and reproducibility
* Data Visualization - planned (charts and dashboards)

## Analytical Approach

### 1\. Exploratory Data Analysis (EDA)

EDA was used to understand baseline delay behavior and identify where meaningful variance exists.



Key findings from EDA:



* Flight delays follow a **right‑skewed (long‑tail) distribution** --> the median delay was 0 minutes, while the worst 1% of flights exceeded ~3 hours of delay
* Origin airport effects **explain more delay variability** than airline choice alone
* Airline performance is **context‑dependent** and varies significantly by airport



### 2\. SQL Modeling \& Analytical Views

EDA findings were formalized into a reproducible SQL analytics layer built on top of a cleaned fact table.

Key SQL views include:



* **Overall delay KPIs** (baseline delay rate and severity)
* **Airline‑level performance** (with minimum flight thresholds)
* **Origin airport performance**
* **Airline × airport interaction analysis**
* **Decomposition view** (airline baseline performance x airport baseline delay environment x interaction effects between the two)



## Key Questions Addressed So Far

* What does the overall distribution of flight delays look like?
* Are delays primarily driven by airlines or by airports?
* How does the same airline perform differently across airports?



## Project Structure

Project Structure

aviation-delays-analysis/

├── data/

│   └── processed/

│       └── flights\_oct\_2025\_processed.csv

├── python/

│   └── load\_to\_sqlite.py

│   └── make\_delay\_distribution\_plot.py

├── sql/

│   ├── 01\_schema.sql

│   ├── 02\_load\_notes.md

│   ├── 03\_core\_views.sql

│   ├── 04\_ranked\_views.sql

│   ├── 05\_decomposition.sql

│   └── 06\_index\_views.sql

├── viz/

│   └── delay\_distribution\_oct\_2025.png

├── README.md

└── .gitignore



## Next Steps



* Build explanatory data visualizations from core SQL views
* Translate analytical findings into clear, non‑technical insights
* Finalize dashboards and documentation
