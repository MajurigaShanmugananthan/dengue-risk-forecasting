import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

dengue = pd.read_csv(
    BASE_DIR / "data/processed/fixed_dengue_names_clean.csv",
    parse_dates=["week"]
)

climate = pd.read_csv(
    BASE_DIR / "data/processed/fixed_climate_names_clean.csv",
    parse_dates=["week"]
)

merged = dengue.merge(
    climate,
    on=["District", "MOH", "week"],
    how="left"
)

merged.to_csv(
    BASE_DIR / "data/processed/dengue_climate_merged.csv",
    index=False
)

print("✅ Dengue & climate merged")
