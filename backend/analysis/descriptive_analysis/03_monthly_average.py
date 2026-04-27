import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data/processed/fixed_dengue_names_clean.csv"
PLOT_DIR = BASE_DIR / "backend/analysis/plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["week"] = pd.to_datetime(df["week"])

# Extract month
df["month"] = df["week"].dt.month

monthly_avg = df.groupby("month")["Dengue_Cases"].mean()

plt.figure(figsize=(10, 5))
monthly_avg.plot(kind="bar", color="orange")
plt.title("Average Monthly Dengue Cases")
plt.xlabel("Month")
plt.ylabel("Average Dengue Cases")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(PLOT_DIR / "03_monthly_dengue_average.png", dpi=300)
plt.show()
