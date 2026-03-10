import pandas as pd

DATA_PATH = "data/processed/flights_oct_2025_processed.csv"

def fmt_pct(x: float) -> str:
    return f"{x:.2%}"

def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["FL_DATE"])
    print("Loaded processed dataset:", df.shape)

    # --- Origin airport summary ---
    origin = (
        df.groupby("ORIGIN")
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

    # Filter to avoid tiny-airport noise
    MIN_FLIGHTS = 2000
    origin_f = origin[origin["flights"] >= MIN_FLIGHTS].copy()

    print(f"\nOrigin airports total: {origin.shape[0]}")
    print(f"Origin airports with >= {MIN_FLIGHTS} flights: {origin_f.shape[0]}")

    # --- Correct numeric ranking (keep numeric until after sorting) ---
    worst15 = origin_f.sort_values("delay_rate", ascending=False).head(15)
    best15  = origin_f.sort_values("delay_rate", ascending=True).head(15)

    # Format only for display
    worst15_disp = worst15.copy()
    best15_disp  = best15.copy()

    worst15_disp["delay_rate"] = worst15_disp["delay_rate"].map(fmt_pct)
    best15_disp["delay_rate"]  = best15_disp["delay_rate"].map(fmt_pct)

    print("\n--- Worst 15 ORIGIN airports by delay rate (min 2000 flights) ---")
    print(worst15_disp)

    print("\n--- Best 15 ORIGIN airports by delay rate (min 2000 flights) ---")
    print(best15_disp)

    # --- Save outputs ---
    origin_f.sort_values("delay_rate", ascending=False).to_csv("data/processed/eda_origin_summary.csv")
    origin.sort_values("flights", ascending=False).to_csv("data/processed/eda_origin_by_volume.csv")

    print("\n✅ Saved:")
    print(" - data/processed/eda_origin_summary.csv")
    print(" - data/processed/eda_origin_by_volume.csv")

    # --- ATL spotlight ---
    print("\n--- ATL SPOTLIGHT ---")
    if "ATL" in origin.index:
        atl = origin.loc[["ATL"]].copy()
        atl_disp = atl.copy()
        atl_disp["delay_rate"] = atl_disp["delay_rate"].map(fmt_pct)
        print(atl_disp)
    else:
        print("ATL not found as an origin airport in this dataset slice.")

    # --- Compare ATL to overall (helps storytelling) ---
    overall_delay_rate = df["IS_DELAYED"].mean()
    print(f"\nOverall delay rate (all flights): {overall_delay_rate:.2%}")

    if "ATL" in origin.index:
        atl_rate = float(origin.loc["ATL", "delay_rate"])
        diff = atl_rate - overall_delay_rate
        print(f"ATL delay rate: {atl_rate:.2%}  (ATL - overall = {diff:+.2%})")

if __name__ == "__main__":
    main()