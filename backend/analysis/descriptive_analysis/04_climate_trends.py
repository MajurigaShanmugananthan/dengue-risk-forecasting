import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data/processed/fixed_climate_names_clean.csv"
PLOT_DIR = BASE_DIR / "backend/analysis/plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["week"] = pd.to_datetime(df["week"])

df_weekly = df.groupby("week").agg({
    "tavg": "mean",
    "prcp": "mean"
}).reset_index()

plt.figure(figsize=(12, 6))
plt.plot(df_weekly["week"], df_weekly["tavg"], label="Avg Temperature")
plt.plot(df_weekly["week"], df_weekly["prcp"], label="Rainfall")
plt.legend()
plt.title("Climate Variable Trends Over Time")
plt.xlabel("Week")
plt.ylabel("Value")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(PLOT_DIR / "04_climate_trends.png", dpi=300)
plt.show()
