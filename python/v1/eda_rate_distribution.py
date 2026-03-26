import pandas as pd

df = pd.read_csv(
    "data/processed/flights_oct_2025_processed.csv",
    parse_dates=["FL_DATE"]
)

print("Dataset shape:", df.shape)

# ----------------------------
# Overall delay rate
# ----------------------------
overall_delay_rate = df["IS_DELAYED"].mean()
print(f"\nOverall delay rate (ARR_DELAY ≥ 15 min): {overall_delay_rate:.2%}")

# ----------------------------
# Arrival delay distribution
# ----------------------------
print("\nArrival delay (clean) distribution summary (minutes):")
print(
    df["ARR_DELAY_CLEAN"].describe(
        percentiles=[0.5, 0.75, 0.9, 0.95, 0.99]
    )
)