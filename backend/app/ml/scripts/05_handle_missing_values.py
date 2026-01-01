import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
INPUT_FILE = BASE_DIR / "data/processed/dengue_climate_merged.csv"
OUTPUT_FILE = BASE_DIR / "data/processed/dengue_climate_filled.csv"

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv(INPUT_FILE, parse_dates=["week"])

# --------------------------------------------------
# Fill missing dengue cases
# --------------------------------------------------
df["Dengue_Cases"] = df["Dengue_Cases"].fillna(0)

# --------------------------------------------------
# Climate columns
# --------------------------------------------------
climate_cols = ["tavg", "tmin", "tmax", "prcp", "wspd"]

# Ensure numeric
df[climate_cols] = df[climate_cols].apply(pd.to_numeric, errors="coerce")

# --------------------------------------------------
# Interpolate climate values PER MOH (SAFE WAY)
# --------------------------------------------------
df = df.sort_values(["District", "MOH", "week"])

for col in climate_cols:
    df[col] = (
        df.groupby(["District", "MOH"])[col]
          .transform(lambda x: x.interpolate(limit_direction="both"))
    )

# --------------------------------------------------
# Save
# --------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Missing values handled correctly (no index errors)")
print(f"📁 Saved to: {OUTPUT_FILE}")
