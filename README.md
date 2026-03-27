# U.S. Aviation Delays Analysis

## Project Overview

This project analyzes U.S. domestic airline flight data to answer a question that impacts consumer travel and airport business operations: What are the primary drivers of flight delays, and how, if at all, does that delay behavior vary across **airlines**, **airports**, and the **interactions** between the two?

Rather than focusing solely on rankings, the goal is to understand *where delay variability originates* and why certain flights experience severe disruptions while most do not.

## Dataset

**Source:** U.S. Bureau of Transportation Statistics (BTS) – Airline On‑Time Performance Data

**Scope:** Domestic U.S. flights (October 2025)



The dataset provides flight‑level records including carrier, origin airport, timing, and arrival delay information. Keeping the scope to one month allowed for deeper exploratory analyst while still working with a large, production-scale dataset (\~600k flights).

## Tools

* Python - data cleaning and exploratory data analysis (EDA)
* SQL (SQLite) - data modeling, aggregation, and analytical views
* Tableau - interactive dashboards and visual analysis
* Git/GitHub - version control and reproducibility



## Analytical Approach

### 1\. Exploratory Data Analysis (EDA)

EDA was used to understand baseline delay behavior and identify where meaningful variance exists. The analysis was concentrated over 14 distinct airline carriers and 346 distinct origin airports.



Key findings \& insights from EDA:



* Just a **little over 20%** of total flights were delayed, suggesting that stories of constant delays are overblown
* Flight delays follow a **right‑skewed (long‑tail) distribution** {p90 = 40 mins, p95 = 75, p99 = 192} --> so while rare, severe delays dominate averages
* Delay variance between airline carriers was **moderate (\~9% spread)** --> airline operations matter, but are not entirely influential to delay behavior
* Delay variance between origin carriers was more prominent (\~21% spread) --> this suggests that origin airport effects **explain more delay variability** than airline choice alone
* Composition analysis (airline x airport) showed that airline performance is **context‑dependent** and varies significantly by airport --> combinations provide more explanation rather than each single factor alone



### 2\. SQL Modeling \& Analytical Views

EDA findings were formalized into reproducible SQL views built on top of a cleaned fact table.



Key SQL views include:



* **Overall delay KPIs** (baseline delay rate and severity)
* **Airline‑level performance** (with minimum flight thresholds)
* **Origin airport performance**
* **Airline × airport interaction analysis**
* **Decomposition view** (airline baseline performance x airport baseline delay environment x interaction effects between the two)
* Delay behavior by flight distance (short, medium, long haul), including variability and recovery metrics



### 3\. Data Visualization

Two Tableau dashboards were created to translate SQL insights into interpretable visuals.



**Dashboard 1 — Airlines, Airports, and Interactions**



* Airline‑level delay differences exist, but origin airports introduce more variability.
* Airline performance is not portable across airports.
* Simple “best” or “worst” airline labels break down once airport context is considered.



**Dashboard 2 — Delay Risk and Recovery by Distance**



* Short‑, medium‑, and long‑haul flights exhibit nearly identical average arrival delays, even after excluding NYC airports.
* This suggests airlines actively normalize average arrival performance through schedule design.
* Differences emerge beneath the averages:

  * Long‑haul flights recover delay more often and lose less time on average between departure and arrival.
  * However, long‑haul flights exhibit greater volatility when disruptions occur.
  * Short‑haul flights are more consistent but more fragile once delayed.
    
## Key Questions Addressed

* What does the overall distribution of flight delays look like?
* Are delays primarily driven by airlines or by airports?
* How does the same airline perform differently across airports?
* Why do average delay rates look similar across flight distances?
* How do delay risk and recovery behavior differ once a flight is disrupted?



## Project Structure

Project Structure

aviation-delays-analysis/

├── data \[raw/processed CSVs for data analysis]

├── python \[Python scripts for EDA, loading to SQL, etc.]

├── sql \[SQL views from EDA]

├── viz \[Visualization artifacts (charts, dashboards, etc.)

├── README.md

└── .gitignore



## Project Status \& Next Steps

The SQL pipeline and Tableau dashboards represent a completed v1 of this project. Future extensions could explore:



* Weather impacts
* Time‑of‑day effects
* Delay propagation across aircraft rotations
* Carrier‑specific scheduling strategies



For now, the project serves as a completed case study in moving beyond averages to understand system behavior, variability, and operational risk.

