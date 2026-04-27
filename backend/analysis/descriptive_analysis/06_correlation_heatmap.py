import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data/processed/dengue_risk_dataset.csv"
PLOT_DIR = BASE_DIR / "backend/analysis/plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

cols = [
    "Dengue_Cases",
    "prcp",
    "tavg",
    "Dengue_Cases_lag_1",
    "Dengue_Cases_lag_2",
    "Dengue_Cases_lag_3",
    "Dengue_Cases_lag_4"
]

corr = df[cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Dengue & Climate Variables")
plt.tight_layout()

plt.savefig(PLOT_DIR / "06_correlation_heatmap.png", dpi=300)
plt.show()
