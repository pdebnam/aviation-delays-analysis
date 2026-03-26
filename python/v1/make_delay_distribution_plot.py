import os
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = "data/processed/flights_oct_2025_processed.csv"
OUT_DIR = "viz"
OUT_PATH = os.path.join(OUT_DIR, "delay_distribution_oct_2025.png")

# -----------------------------
# Plot settings
# -----------------------------
X_MAX = 250          # keep plot readable; tail is still captured by p99 line
BINS = 120
USE_LOG_Y = True    # set True if you want the long tail to stand out more

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    # Uppercase column names (as you confirmed)
    s = df["ARR_DELAY_CLEAN"].dropna()

    # Percentiles for annotation
    p50 = s.quantile(0.50)
    p90 = s.quantile(0.90)
    p95 = s.quantile(0.95)
    p99 = s.quantile(0.99)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.hist(s, bins=BINS, range=(0, X_MAX), color="#2E86AB", alpha=0.85)

    title = "Arrival Delay Distribution — October 2025"
    plt.title(title, fontsize=14)
    plt.xlabel("Arrival Delay (minutes)")
    plt.ylabel("Number of Flights" + (" (log scale)" if USE_LOG_Y else ""))

    if USE_LOG_Y:
        plt.yscale("log")

    # Vertical percentile lines
    for val, label, color in [
        (p50, f"p50 (median) = {p50:.0f}", "#2F4858"),
        (p90, f"p90 = {p90:.0f}", "#F6AE2D"),
        (p95, f"p95 = {p95:.0f}", "#F26419"),
        (p99, f"p99 = {p99:.0f}", "#D62828"),
    ]:
        plt.axvline(val, linestyle="--", linewidth=2, color=color, label=label)

    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=200)
    plt.close()

    print("✅ Saved plot to:", OUT_PATH)
    print("Percentiles:", {"p50": float(p50), "p90": float(p90), "p95": float(p95), "p99": float(p99)})

if __name__ == "__main__":
    main()