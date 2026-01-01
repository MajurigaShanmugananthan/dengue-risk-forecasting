import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

dengue = pd.read_csv(
    BASE_DIR / "data/processed/dengue_cases_weekly_long.csv",
    parse_dates=["week"]
)

climate = pd.read_csv(
    BASE_DIR / "data/processed/weekly_climate_new_moh_clean.csv",
    parse_dates=["week"]
)

final = dengue.merge(
    climate,
    on=["District", "MOH", "week"],
    how="left"
)

final.to_csv(
    BASE_DIR / "data/processed/dengue_climate_weekly_merged.csv",
    index=False
)

print("✅ Dengue + climate weekly dataset created")
