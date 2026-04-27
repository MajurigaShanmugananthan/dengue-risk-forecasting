import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data/processed/fixed_dengue_names_clean.csv"
PLOT_DIR = BASE_DIR / "backend/analysis/plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)

# Convert week to datetime
df["week"] = pd.to_datetime(df["week"])

# Aggregate dengue cases per week
df_weekly = df.groupby("week")["Dengue_Cases"].sum().reset_index()

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_weekly["week"], df_weekly["Dengue_Cases"], color="red")
plt.title("Weekly Dengue Case Trend")
plt.xlabel("Week")
plt.ylabel("Number of Dengue Cases")
plt.grid(alpha=0.3)
plt.tight_layout()

# Save
plt.savefig(PLOT_DIR / "01_dengue_time_series.png", dpi=300)
plt.show()
