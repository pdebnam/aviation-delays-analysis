
-- ========================================
-- Core analytical views
-- Mirrors EDA findings
-- Overall Delay KPIs
-- Delay Performance by Airline
-- Delay Performance by Airport
-- Delay Performance by Airline x Airport
-- ========================================

-- Overall Delay KPIs

DROP VIEW IF EXISTS vw_overall_delay_kpis;
CREATE VIEW vw_overall_delay_kpis AS
SELECT
	COUNT(*) AS total_flights,
	AVG(is_delayed) AS delay_rate,
	AVG(arr_delay_clean) AS avg_delay_mins
FROM fact_flights;

-- Delay Performance by Airline

DROP VIEW IF EXISTS vw_airline_delay_performance;
CREATE VIEW vw_airline_delay_performance AS
SELECT
	op_unique_carrier AS carrier,
	COUNT(*) AS flights,
	AVG(is_delayed) AS delay_rate,
	AVG(arr_delay_clean) AS avg_delay_mins
FROM fact_flights
GROUP BY op_unique_carrier
HAVING COUNT(*) >= 1000;

-- Delay Performance by Airport

DROP VIEW IF EXISTS vw_airport_delay_performance;
CREATE VIEW vw_airport_delay_performance AS
SELECT
	origin,
	COUNT(*) AS flights,
	AVG(is_delayed) AS delay_rate,
	AVG(arr_delay_clean) AS avg_delay_mins
FROM fact_flights
GROUP BY origin
HAVING COUNT(*) >= 2000;

-- Delay Performance by Airline x Airport

DROP VIEW IF EXISTS vw_airline_x_airport_performance;
CREATE VIEW vw_airline_x_airport_performance AS
SELECT
	origin,
	op_unique_carrier AS carrier,
	COUNT(*) AS flights,
	AVG(is_delayed) AS delay_rate,
	AVG(arr_delay_clean) AS avg_delay_mins
FROM fact_flights
GROUP BY origin,op_unique_carrier
HAVING COUNT(*) >= 300
