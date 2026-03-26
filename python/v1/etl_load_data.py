import pandas as pd

RAW_DATA_PATH = "data/raw/On_Time_2025_10.csv"
PROCESSED_DATA_PATH = "data/processed/flights_oct_2025_processed.csv"

def main():
    print("Loading raw flight data...")
    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Initial shape: {df.shape}")

    # -----------------------------
    # Basic cleaning
    # -----------------------------

    # Convert FL_DATE to datetime
    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])

    # Ensure flags are integers
    df["CANCELLED"] = df["CANCELLED"].astype(int)
    df["DIVERTED"] = df["DIVERTED"].astype(int)

    # -----------------------------
    # Filter to completed flights
    # -----------------------------
    completed_flights = df[
        (df["CANCELLED"] == 0) &
        (df["DIVERTED"] == 0)
    ].copy()

    print(f"Completed flights only: {completed_flights.shape}")

    # -----------------------------
    # Create delay metrics
    # -----------------------------

    # On-time definition: arrival delay < 15 minutes
    completed_flights["IS_DELAYED"] = (
        completed_flights["ARR_DELAY"] >= 15
    ).astype(int)

    # Clip early arrivals to 0 for cleaner averages
    completed_flights["ARR_DELAY_CLEAN"] = completed_flights["ARR_DELAY"].clip(lower=0)

    # -----------------------------
    # Select final columns
    # -----------------------------
    final_columns = [
        "FL_DATE",
        "YEAR",
        "MONTH",
        "DAY_OF_WEEK",
        "OP_UNIQUE_CARRIER",
        "ORIGIN",
        "DEST",
        "DISTANCE",
        "DEP_DELAY",
        "ARR_DELAY_CLEAN",
        "IS_DELAYED"
    ]

    final_df = completed_flights[final_columns]

    

# -----------------------------
    # Data quality checks
    # -----------------------------
    print("\n--- DATA QUALITY CHECKS ---")

    # 1. Null checks on critical fields
    critical_columns = [
        "FL_DATE",
        "OP_UNIQUE_CARRIER",
        "ORIGIN",
        "DEST",
        "ARR_DELAY_CLEAN",
        "IS_DELAYED"
    ]

    null_counts = final_df[critical_columns].isnull().sum()

    print("\nNull value counts (critical columns):")
    print(null_counts)

    # 2. Duplicate row check
# -----------------------------
    # Deduplicate identical rows
    # -----------------------------
    before_dedup = final_df.shape[0]

    final_df = final_df.drop_duplicates()

    after_dedup = final_df.shape[0]

    print(
        f"\nDeduplication complete: "
        f"removed {before_dedup - after_dedup} duplicate rows"
    )

    duplicate_count = final_df.duplicated().sum()
    print(f"\nDuplicate rows found: {duplicate_count}")



    # 3. Delay flag sanity check
    delay_rate = final_df["IS_DELAYED"].mean()
    print(f"\nOverall delay rate: {delay_rate:.2%}")

    # 4. Arrival delay range check
    print("\nArrival delay (clean) summary:")
    print(final_df["ARR_DELAY_CLEAN"].describe())

    print(f"Final dataset shape post quality check: {final_df.shape}")
    # -----------------------------
    # Write processed data
    # -----------------------------
    final_df.to_csv(PROCESSED_DATA_PATH, index=False)

    print(f"\n✅ Processed data written to: {PROCESSED_DATA_PATH}")

    print("\nSample processed rows:")
    print(final_df.head())

if __name__ == "__main__":
    main()