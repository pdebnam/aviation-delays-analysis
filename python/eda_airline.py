import pandas as pd

DATA_PATH = "data/processed/flights_oct_2025_processed.csv"

def fmt_pct(x: float) -> str:
    return f"{x:.2%}"

def main():
    # Load processed dataset
    df = pd.read_csv(DATA_PATH, parse_dates=["FL_DATE"])
    print("Loaded processed dataset:", df.shape)

    # --- Airline summary table ---
    airline = (
        df.groupby("OP_UNIQUE_CARRIER")
          .agg(
              flights=("IS_DELAYED", "size"),
              delay_rate=("IS_DELAYED", "mean"),
              mean_delay=("ARR_DELAY_CLEAN", "mean"),
              median_delay=("ARR_DELAY_CLEAN", "median"),
              p90=("ARR_DELAY_CLEAN", lambda s: s.quantile(0.90)),
              p95=("ARR_DELAY_CLEAN", lambda s: s.quantile(0.95)),
              p99=("ARR_DELAY_CLEAN", lambda s: s.quantile(0.99)),
          )
    )

    # Filter small-sample carriers so rankings are meaningful
    MIN_FLIGHTS = 1000
    airline_f = airline[airline["flights"] >= MIN_FLIGHTS].copy()

    print(f"\nAirlines total: {airline.shape[0]}")
    print(f"Airlines with >= {MIN_FLIGHTS} flights: {airline_f.shape[0]}")

    # ------------------------------------------------------------
    # ✅ Correct numeric ranking (DO NOT format before sorting)
    # ------------------------------------------------------------
    worst10 = airline_f.sort_values("delay_rate", ascending=False).head(10)
    best10  = airline_f.sort_values("delay_rate", ascending=True).head(10)

    # Format ONLY for printing (after selecting top/bottom)
    worst10_disp = worst10.copy()
    best10_disp = best10.copy()

    worst10_disp["delay_rate"] = worst10_disp["delay_rate"].map(fmt_pct)
    best10_disp["delay_rate"] = best10_disp["delay_rate"].map(fmt_pct)

    print("\n--- Worst 10 airlines by delay rate (min 1000 flights) ---")
    print(worst10_disp)

    print("\n--- Best 10 airlines by delay rate (min 1000 flights) ---")
    print(best10_disp)

    # ------------------------------------------------------------
    # Save outputs for later use (SQL / Power BI / Tableau)
    # ------------------------------------------------------------
    airline_f_sorted = airline_f.sort_values("delay_rate", ascending=False)
    airline_f_sorted.to_csv("data/processed/eda_airline_summary.csv")
    print("\n✅ Saved: data/processed/eda_airline_summary.csv")

    airline_by_volume = airline.sort_values("flights", ascending=False)
    airline_by_volume.to_csv("data/processed/eda_airline_by_volume.csv")
    print("✅ Saved: data/processed/eda_airline_by_volume.csv")


if __name__ == "__main__":
    main()