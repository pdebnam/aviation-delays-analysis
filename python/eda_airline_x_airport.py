import pandas as pd

DATA_PATH = "data/processed/flights_oct_2025_processed.csv"

def fmt_pct(x: float) -> str:
    return f"{x:.2%}"

def main():
    # -----------------------------
    # Load data
    # -----------------------------
    df = pd.read_csv(DATA_PATH, parse_dates=["FL_DATE"])
    print("Loaded processed dataset:", df.shape)

    # -----------------------------
    # Airports to analyze (Option B)
    # -----------------------------
    airports = ["ATL", "LGA", "ORD", "DFW", "EWR", "JFK", "BOS"]

    df_sub = df[df["ORIGIN"].isin(airports)].copy()
    print(f"Filtered to airports {airports}: {df_sub.shape}")

    # -----------------------------
    # Airline × Airport aggregation
    # -----------------------------
    axa = (
        df_sub
        .groupby(["ORIGIN", "OP_UNIQUE_CARRIER"])
        .agg(
            flights=("IS_DELAYED", "size"),
            delay_rate=("IS_DELAYED", "mean"),
            mean_delay=("ARR_DELAY_CLEAN", "mean"),
            p95=("ARR_DELAY_CLEAN", lambda s: s.quantile(0.95)),
            p99=("ARR_DELAY_CLEAN", lambda s: s.quantile(0.99)),
        )
        .reset_index()
    )

    # -----------------------------
    # Filter small samples
    # -----------------------------
    MIN_FLIGHTS = 300
    axa_f = axa[axa["flights"] >= MIN_FLIGHTS].copy()
    print(f"Combos with >= {MIN_FLIGHTS} flights:", axa_f.shape[0])

    # -----------------------------
    # Save long-format output
    # -----------------------------
    axa_f.sort_values(
        ["ORIGIN", "delay_rate"],
        ascending=[True, False]
    ).to_csv(
        "data/processed/eda_airline_x_airport.csv",
        index=False
    )

    print("✅ Saved: data/processed/eda_airline_x_airport.csv")

    # -----------------------------
    # Pivot tables (for inspection)
    # -----------------------------
    pivot_rate = axa_f.pivot(
        index="ORIGIN",
        columns="OP_UNIQUE_CARRIER",
        values="delay_rate"
    )

    pivot_p95 = axa_f.pivot(
        index="ORIGIN",
        columns="OP_UNIQUE_CARRIER",
        values="p95"
    )

    pivot_n = axa_f.pivot(
        index="ORIGIN",
        columns="OP_UNIQUE_CARRIER",
        values="flights"
    )

    print("\n--- Delay Rate Pivot (ORIGIN x CARRIER) ---")
    print(
        pivot_rate.apply(
            lambda col: col.map(
                lambda x: fmt_pct(x) if pd.notnull(x) else ""
            )
        )
    )

    print("\n--- P95 Delay (minutes) Pivot (ORIGIN x CARRIER) ---")
    print(pivot_p95.round(1))

    print("\n--- Flights Count Pivot (ORIGIN x CARRIER) ---")
    print(pivot_n.fillna(0).astype(int))

    # -----------------------------
    # Worst airlines within each airport
    # -----------------------------
    print("\n--- Top 5 WORST airlines within each airport (by delay_rate) ---")
    for airport in airports:
        subset = (
            axa_f[axa_f["ORIGIN"] == airport]
            .sort_values("delay_rate", ascending=False)
            .head(5)
        )

        if subset.empty:
            continue

        subset_disp = subset.copy()
        subset_disp["delay_rate"] = subset_disp["delay_rate"].map(fmt_pct)

        print(f"\nAirport: {airport}")
        print(
            subset_disp[
                ["OP_UNIQUE_CARRIER", "flights", "delay_rate", "mean_delay", "p95", "p99"]
            ]
        )

    # -----------------------------
    # Focus airlines across airports
    # -----------------------------
    focus_airlines = ["DL", "AA", "UA", "WN", "B6"]

    print("\n--- Focus airlines across airports (delay_rate + p95) ---")

    focus = axa_f[axa_f["OP_UNIQUE_CARRIER"].isin(focus_airlines)].copy()
    focus["delay_rate"] = focus["delay_rate"].map(fmt_pct)

    print(
        focus
        .sort_values(["OP_UNIQUE_CARRIER", "ORIGIN"])
        [
            ["OP_UNIQUE_CARRIER", "ORIGIN", "flights", "delay_rate", "p95", "p99"]
        ]
    )

if __name__ == "__main__":
    main()