import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data/processed/dengue_risk_dataset.csv"
PLOT_DIR = BASE_DIR / "backend/analysis/plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["week"] = pd.to_datetime(df["week"])

df_weekly = df.groupby("week").agg({
    "Dengue_Cases": "sum",
    "prcp": "mean"
}).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(df_weekly["week"], df_weekly["Dengue_Cases"], color="red")
ax1.set_xlabel("Week")
ax1.set_ylabel("Dengue Cases", color="red")

ax2 = ax1.twinx()
ax2.plot(df_weekly["week"], df_weekly["prcp"], color="blue", alpha=0.6)
ax2.set_ylabel("Rainfall (mm)", color="blue")

plt.title("Dengue Cases vs Rainfall")
fig.tight_layout()

plt.savefig(PLOT_DIR / "02_rainfall_vs_dengue.png", dpi=300)
plt.show()
