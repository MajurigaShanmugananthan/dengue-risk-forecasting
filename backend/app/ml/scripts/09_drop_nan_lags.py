import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

train = pd.read_csv(BASE_DIR / "data/processed/train.csv")
test = pd.read_csv(BASE_DIR / "data/processed/test.csv")

# Drop rows with any NaN values
train_clean = train.dropna()
test_clean = test.dropna()

train_clean.to_csv(BASE_DIR / "data/processed/train_clean.csv", index=False)
test_clean.to_csv(BASE_DIR / "data/processed/test_clean.csv", index=False)

print("✅ Rows with NaN lag values removed")
