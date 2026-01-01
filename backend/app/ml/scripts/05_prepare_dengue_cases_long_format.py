import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
INPUT_FILE = BASE_DIR / "data/raw/Dengue Case Notification 2013 to 2022.xlsx"
OUTPUT_FILE = BASE_DIR / "data/processed/dengue_cases_weekly_long.csv"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

excel_file = pd.ExcelFile(INPUT_FILE)
sheet_names = excel_file.sheet_names

all_years = []

for sheet in sheet_names:
    if sheet == "Sheet1":
        continue

    print(f"⬇ Processing year: {sheet}")

    df = pd.read_excel(INPUT_FILE, sheet_name=sheet)

    id_cols = ["District", "MOH"]

    # All columns except District, MOH, Total are week start dates
    date_cols = [
        c for c in df.columns
        if c not in id_cols and str(c).lower() != "total"
    ]

    long_df = df.melt(
        id_vars=id_cols,
        value_vars=date_cols,
        var_name="week",
        value_name="Dengue_Cases"
    )

    # Convert week column to datetime
    long_df["week"] = pd.to_datetime(long_df["week"], errors="coerce")

    # Drop invalid weeks
    long_df = long_df.dropna(subset=["week"])

    # Replace missing dengue counts with 0
    long_df["Dengue_Cases"] = long_df["Dengue_Cases"].fillna(0).astype(int)

    all_years.append(
        long_df[["District", "MOH", "week", "Dengue_Cases"]]
    )

final_df = pd.concat(all_years, ignore_index=True)

final_df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ Dengue cases prepared using weekly DATE alignment")
print(f"📁 Saved to: {OUTPUT_FILE}")
