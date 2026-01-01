import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
df = pd.read_csv(
    BASE_DIR / "data/processed/dengue_risk_dataset.csv",
    parse_dates=["week"]
)

train = df[df["week"] < "2021-01-01"]
test = df[df["week"] >= "2021-01-01"]

train.to_csv(BASE_DIR / "data/processed/train.csv", index=False)
test.to_csv(BASE_DIR / "data/processed/test.csv", index=False)

print("✅ Time-based train/test split done")
