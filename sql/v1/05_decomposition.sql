-- ========================================
-- Airline x Airport Decomposition View
-- Compare each airline-at-airport combo to:
-- that airline’s overall performance
-- that airport’s overall performance
-- ========================================

DROP VIEW IF EXISTS vw_airline_airport_decomposition; 
CREATE VIEW vw_airline_airport_decomposition AS
WITH combo AS (
  SELECT
    origin,
    carrier,
    flights,
    delay_rate,
    avg_delay_mins
  FROM vw_airline_x_airport_performance
),
airline AS (
  SELECT
    carrier,
    delay_rate AS airline_delay_rate,
    avg_delay_mins AS airline_avg_delay_mins
  FROM vw_airline_delay_performance
),
airport AS (
  SELECT
    origin,
    AVG(is_delayed) AS airport_delay_rate,
    AVG(arr_delay_clean) AS airport_avg_delay_mins
  FROM fact_flights
  GROUP BY origin
  HAVING COUNT(*) >= 2000
)
SELECT
  c.origin,
  c.carrier,
  c.flights,
  c.delay_rate AS combo_delay_rate,
  c.avg_delay_mins AS combo_avg_delay_mins,
  a.airline_delay_rate,
  ap.airport_delay_rate,
  (c.delay_rate - a.airline_delay_rate) AS vs_airline_delta,
  (c.delay_rate - ap.airport_delay_rate) AS vs_airport_delta
FROM combo c
LEFT JOIN airline a ON c.carrier = a.carrier
LEFT JOIN airport ap ON c.origin = ap.origin;