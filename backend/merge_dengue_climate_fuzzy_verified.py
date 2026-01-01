import pandas as pd
import os
from fuzzywuzzy import process

# ==============================
# 📂 File Paths
# ==============================
dengue_file = r"E:\dengue_project\data\raw\Dengue Case Notification 2013 to 2022 (UOC Piyumi) UP (2) - Copy.xlsx"
climate_file = r"E:\dengue_project\data\processed\weekly_climate_data_2013_2022.xlsx"

print("📂 Loading data files...")

# ==============================
# 🦟 Step 1: Load All Dengue Sheets
# ==============================
excel = pd.ExcelFile(dengue_file)
year_sheets = [s for s in excel.sheet_names if s.isdigit()]

all_dengue = []

for sheet in year_sheets:
    df = pd.read_excel(dengue_file, sheet_name=sheet, header=3)

    # uniform column names
    df.columns = df.columns.str.strip()

    # fix missing Admin_Area
    if "Admin_Area" in df.columns:
        df["Admin_Area"] = df["Admin_Area"].ffill()
    else:
        df["Admin_Area"] = None

    df["District"] = df["District"].ffill()
    df["Year"] = int(sheet)

    # CASE 1: 2013–2020 wide weekly format
    week_cols = [c for c in df.columns if c.startswith("Week ")]

    if len(week_cols) > 0:
        df_long = df.melt(
            id_vars=["District", "Admin_Area", "MOH", "Year"],
            value_vars=week_cols,
            var_name="Week",
            value_name="Dengue_Cases"
        )
        df_long["Week"] = df_long["Week"].str.extract("(\d+)").astype(int)

    else:
        # CASE 2: 2021–2022 long format
        df_long = df.rename(columns={
            "Week": "Week",
            "Total": "Dengue_Cases"
        })
        df_long = df_long[["District", "Admin_Area", "MOH", "Year", "Week", "Dengue_Cases"]]

    df_long["Dengue_Cases"] = df_long["Dengue_Cases"].fillna(0)
    all_dengue.append(df_long)

dengue_long = pd.concat(all_dengue, ignore_index=True)

print(f"🦟 Dengue rows combined: {len(dengue_long):,}")

# ==============================
# 🌦 Load Climate Data
# ==============================
climate = pd.read_excel(climate_file)
climate.rename(columns={"week": "Week"}, inplace=True)

print(f"🌡 Climate rows: {len(climate):,}")

# ==============================
# 🧩 Fuzzy MOH Matching
# ==============================
dengue_mohs = sorted(dengue_long["MOH"].dropna().unique())
climate_mohs = sorted(climate["MOH"].dropna().unique())

mapping = []
for moh in dengue_mohs:
    match, score = process.extractOne(moh, climate_mohs)
    mapping.append({
        "Dengue_MOH": moh,
        "Matched_MOH": match if score >= 85 else None,
        "Similarity": score
    })

mapping_df = pd.DataFrame(mapping)

# create dictionary
mapping_dict = {
    row["Dengue_MOH"]: row["Matched_MOH"] if row["Matched_MOH"] else row["Dengue_MOH"]
    for _, row in mapping_df.iterrows()
}

# apply fuzzy mapping
dengue_long["MOH"] = dengue_long["MOH"].map(mapping_dict)

# ==============================
# 🔗 Merge With Outer Join
# ==============================
merged = pd.merge(
    dengue_long,
    climate,
    on=["District", "MOH", "Year", "Week"],
    how="outer"
)

merged["Dengue_Cases"] = merged["Dengue_Cases"].fillna(0)

# ==============================
# 💾 Save Outputs
# ==============================
output_dir = r"E:\dengue_project\data\processed"
os.makedirs(output_dir, exist_ok=True)

merged_path = os.path.join(output_dir, "merged_dengue_climate_verified.xlsx")
mapping_path = os.path.join(output_dir, "moh_fuzzy_mapping.xlsx")

merged.to_excel(merged_path, index=False)
mapping_df.to_excel(mapping_path, index=False)

print("\n✅ MERGE COMPLETE!")
print(f"📊 Final merged rows: {len(merged):,}")
print(f"📄 Saved merged file: {merged_path}")
print(f"📄 Saved fuzzy report: {mapping_path}")
