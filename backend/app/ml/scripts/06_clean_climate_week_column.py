import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
INPUT_FILE = BASE_DIR / "data/processed/weekly_climate_new_moh.csv"
OUTPUT_FILE = BASE_DIR / "data/processed/weekly_climate_new_moh_clean.csv"

df = pd.read_csv(INPUT_FILE)

df["week"] = pd.to_datetime(df["week"], errors="coerce")

df.to_csv(OUTPUT_FILE, index=False)

print("✅ Climate week column standardized")
