import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
df = pd.read_csv(BASE_DIR / "data/processed/dengue_climate_lagged.csv")

def risk_label(x):
    if x <= 5:
        return 0  # Low
    elif x <= 20:
        return 1  # Medium
    else:
        return 2  # High

df["Risk_Level"] = df["Dengue_Cases"].apply(risk_label)

df.to_csv(
    BASE_DIR / "data/processed/dengue_risk_dataset.csv",
    index=False
)

print("✅ Risk labels created")
