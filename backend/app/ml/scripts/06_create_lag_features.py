import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
df = pd.read_csv(
    BASE_DIR / "data/processed/dengue_climate_filled.csv",
    parse_dates=["week"]
)

df = df.sort_values(["District", "MOH", "week"])

lags = [1, 2, 3, 4]
cols = ["Dengue_Cases", "prcp", "tavg"]

for lag in lags:
    for col in cols:
        df[f"{col}_lag_{lag}"] = (
            df.groupby(["District", "MOH"])[col].shift(lag)
        )

df.to_csv(
    BASE_DIR / "data/processed/dengue_climate_lagged.csv",
    index=False
)

print("✅ Lag features created")
