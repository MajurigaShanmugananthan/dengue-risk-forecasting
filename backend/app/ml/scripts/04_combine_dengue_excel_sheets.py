import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[4]
INPUT_FILE = BASE_DIR / "data/raw/Dengue Case Notification 2013 to 2022.xlsx"
OUTPUT_FILE = BASE_DIR / "data/processed/dengue_cases_2013_2022_combined.csv"

# Ensure output directory exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Read Excel file and get all sheet names
# --------------------------------------------------
excel_file = pd.ExcelFile(INPUT_FILE)
sheet_names = excel_file.sheet_names

print("📄 Sheets found in Excel file:")
print(sheet_names)

all_dfs = []

# --------------------------------------------------
# Read each sheet and append
# --------------------------------------------------
for sheet in sheet_names:
    print(f"⬇ Reading sheet: {sheet}")

    df = pd.read_excel(INPUT_FILE, sheet_name=sheet)

    # Add sheet name as a column (important for traceability)
    df["Source_Sheet"] = sheet

    all_dfs.append(df)

# --------------------------------------------------
# Combine all sheets row-wise
# --------------------------------------------------
combined_df = pd.concat(all_dfs, ignore_index=True)

# --------------------------------------------------
# Save combined dataset
# --------------------------------------------------
combined_df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ All sheets combined successfully!")
print(f"📁 Output saved at: {OUTPUT_FILE}")
