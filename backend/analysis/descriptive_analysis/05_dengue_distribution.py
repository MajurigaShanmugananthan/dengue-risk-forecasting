import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data/processed/fixed_dengue_names_clean.csv"
PLOT_DIR = BASE_DIR / "backend/analysis/plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

plt.figure(figsize=(8, 5))
plt.hist(df["Dengue_Cases"], bins=30, color="purple", alpha=0.7)
plt.title("Distribution of Dengue Cases")
plt.xlabel("Dengue Cases")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(PLOT_DIR / "05_dengue_distribution.png", dpi=300)
plt.show()

