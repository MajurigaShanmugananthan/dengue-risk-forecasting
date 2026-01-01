import pandas as pd
from pathlib import Path
from utils import clean_filename

BASE_DIR = Path(__file__).resolve().parents[4]
WEEKLY_DIR = BASE_DIR / "data/processed/climate_weekly"
REF_FILE = BASE_DIR / "data/reference/colombo_moh_coordinates.csv"
OUTPUT_FILE = WEEKLY_DIR / "weekly_climate_new_moh.csv"

ref_df = pd.read_csv(REF_FILE)

all_weekly = []

for _, row in ref_df.iterrows():
    district = clean_filename(row["District"])
    moh = clean_filename(row["MOH"])

    file_name = f"{district}_{moh}_weekly.csv"
    file_path = WEEKLY_DIR / file_name

    if file_path.exists():
        df = pd.read_csv(file_path)
        all_weekly.append(df)
    else:
        print(f"⚠ Missing file: {file_name}")

final_df = pd.concat(all_weekly, ignore_index=True)
final_df.to_csv(OUTPUT_FILE, index=False)

print("✅ Final weekly dataset created in CSV order.")
