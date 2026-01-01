import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

files = [
    "dengue_names_clean.csv",
    "climate_names_clean.csv"
]

for f in files:
    df = pd.read_csv(BASE_DIR / f"data/processed/{f}")
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    df.to_csv(BASE_DIR / f"data/processed/fixed_{f}", index=False)

print("✅ Week column standardized to datetime")
