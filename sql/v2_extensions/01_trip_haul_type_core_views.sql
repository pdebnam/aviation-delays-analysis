-- ==========================================================================
-- Views to compare arrival delays by trip haul type
-- Hauls: Short - < 500 miles
--        Medium - 500 < 1500 miles
--        Long - > 1500 miles
-- For this analysis, excluded NYC airports (EWR, LGA, JFK) due to congestion
-- in NYC airspace possibly causing distortion
-- This is due to congestion in the NYC airspace possibly causing distortion
-- ==========================================================================
DROP VIEW IF EXISTS vw_arrival_delay_by_haul_type_overall;
CREATE VIEW vw_arrival_delay_by_haul_type_overall AS
WITH flights_nyc AS (
	SELECT
		CASE
			WHEN distance < 500 THEN 'Short'
			WHEN distance < 1500 THEN 'Medium'
			ELSE 'Long'
		END AS trip_haul,
		COUNT(*) AS flights,
		ROUND(AVG(distance),2) AS avg_distance,	
		ROUND(AVG(is_delayed),2) AS delay_rate
	FROM fact_flights
	GROUP BY trip_haul
	),
flights_ex_nyc AS (
	SELECT
		CASE
			WHEN distance < 500 THEN 'Short'
			WHEN distance < 1500 THEN 'Medium'
			ELSE 'Long'
		END AS trip_haul,
		COUNT(*) AS flights,
		ROUND(AVG(distance),2) AS avg_distance,	
		ROUND(AVG(is_delayed),2) AS delay_rate
	FROM fact_flights
	WHERE origin NOT IN ('EWR','JFK','LGA')
	GROUP BY trip_haul
	)
SELECT
	n.trip_haul,
	n.flights AS flights_nyc,
	f.flights AS flights_ex_nyc,
	n.avg_distance AS avg_distance_nyc,
	f.avg_distance AS avg_distance_ex_nyc,
	n.delay_rate AS avg_delay_rate_nyc,
	f.delay_rate AS avg_delay_rate_ex_nyc
FROM flights_nyc AS n
JOIN flights_ex_nyc AS f ON n.trip_haul = f.trip_haul;
	
SELECT *
FROM vw_arrival_delay_by_haul_type_overall;	

