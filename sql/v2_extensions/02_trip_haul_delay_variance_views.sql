DROP VIEW IF EXISTS vw_delay_variance_recovery_by_haul;

CREATE VIEW vw_delay_variance_recovery_by_haul AS
WITH base_flights AS (
    SELECT
        CASE
            WHEN distance < 500 THEN 'Short'
            WHEN distance < 1500 THEN 'Medium'
            ELSE 'Long'
        END AS trip_haul,
        origin,
		dep_delay,
		arr_delay_clean,        
        (dep_delay - arr_delay_clean) AS recovery_minutes
    FROM fact_flights
),
nyc AS (
    SELECT
        trip_haul,
        COUNT(*) AS flights,
        ROUND(AVG(arr_delay_clean), 2) AS avg_arr_delay,
        ROUND(SQRT(AVG(arr_delay_clean * arr_delay_clean ) - AVG(arr_delay_clean ) * AVG(arr_delay_clean )),2) AS std_arr_delay,
        ROUND(AVG(recovery_minutes), 2) AS avg_recovery_minutes,
        ROUND(AVG(CASE WHEN recovery_minutes > 0 THEN 1 ELSE 0 END), 3) AS pct_recovered,
        ROUND(AVG(CASE WHEN recovery_minutes < 0 THEN 1 ELSE 0 END), 3) AS pct_worsened
    FROM base_flights
    GROUP BY trip_haul
),
ex_nyc AS (
    SELECT
        trip_haul,
        COUNT(*) AS flights,
        ROUND(AVG(arr_delay_clean), 2) AS avg_arr_delay,
        ROUND(SQRT(AVG(arr_delay_clean  * arr_delay_clean ) - AVG(arr_delay_clean ) * AVG(arr_delay_clean )),2) AS std_arr_delay,
        ROUND(AVG(recovery_minutes), 2) AS avg_recovery_minutes,
        ROUND(AVG(CASE WHEN recovery_minutes > 0 THEN 1 ELSE 0 END), 3) AS pct_recovered,
        ROUND(AVG(CASE WHEN recovery_minutes < 0 THEN 1 ELSE 0 END), 3) AS pct_worsened
    FROM base_flights
    WHERE origin NOT IN ('EWR','JFK','LGA')
    GROUP BY trip_haul
)
SELECT
    n.trip_haul,

    n.flights AS flights_nyc,
    e.flights AS flights_ex_nyc,

    n.avg_arr_delay AS avg_arr_delay_nyc,
    e.avg_arr_delay AS avg_arr_delay_ex_nyc,

    n.std_arr_delay AS std_arr_delay_nyc,
    e.std_arr_delay AS std_arr_delay_ex_nyc,

    n.avg_recovery_minutes AS avg_recovery_nyc,
    e.avg_recovery_minutes AS avg_recovery_ex_nyc,

    n.pct_recovered AS pct_recovered_nyc,
    e.pct_recovered AS pct_recovered_ex_nyc,

    n.pct_worsened AS pct_worsened_nyc,
    e.pct_worsened AS pct_worsened_ex_nyc
FROM nyc n
JOIN ex_nyc e
  ON n.trip_haul = e.trip_haul;
  
SELECT *
FROM vw_delay_variance_recovery_by_haul;