-- ========================================
-- Ranked Views
-- Ranks airlines and airports by best, worst, and quartiles
-- ========================================

-- Airlines ranked
DROP VIEW IF EXISTS vw_airline_ranked;
CREATE VIEW vw_airline_ranked AS
	WITH base AS(
		SELECT
			carrier,
			flights,
			delay_rate,
			avg_delay_mins
		FROM vw_airline_delay_performance
		) 
	SELECT 
		carrier,
		flights,
		delay_rate,
		avg_delay_mins,
		ROW_NUMBER() OVER(ORDER BY delay_rate ASC) AS rank_best,
		ROW_NUMBER() OVER(ORDER BY delay_rate DESC) AS rank_worst,
		NTILE(4) OVER(ORDER BY delay_rate) AS quartile_best
	FROM base;

-- Airports ranked
DROP VIEW IF EXISTS vw_airport_ranked;
CREATE VIEW vw_airport_ranked AS
	WITH base AS(
		SELECT
			origin,
			flights,
			delay_rate,
			avg_delay_mins
		FROM vw_airport_delay_performance
	)
	SELECT 
		origin,
		flights,
		delay_rate,
		avg_delay_mins,
		ROW_NUMBER() OVER(ORDER BY delay_rate ASC) AS rank_best,
		ROW_NUMBER() OVER(ORDER BY delay_rate DESC) AS rank_worst,
		NTILE(4) OVER(ORDER BY delay_rate ASC) as quartile_best
	FROM base;