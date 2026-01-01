import pandas as pd

# ==============================
# 1. LOAD DENGUE EXCEL FILE
# ==============================

excel_path = "Dengue Case Notification 2013 to 2022.xlsx"

# Read all sheets (each year)
sheets = pd.read_excel(excel_path, sheet_name=None)

all_years = []

# ==============================
# 2. PROCESS EACH SHEET
# ==============================

for year, df in sheets.items():

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Ensure first two columns are District and MOH
    df.rename(columns={
        df.columns[0]: "District",
        df.columns[1]: "MOH"
    }, inplace=True)

    # Identify week columns (everything except District & MOH)
    week_columns = df.columns.difference(["District", "MOH"])

    # Convert wide → long format
    long_df = df.melt(
        id_vars=["District", "MOH"],
        value_vars=week_columns,
        var_name="Week",
        value_name="Dengue_Cases"
    )

    # Add Year column
    long_df["Year"] = int(year)

    all_years.append(long_df)

# ==============================
# 3. COMBINE ALL YEARS
# ==============================

dengue_long = pd.concat(all_years, ignore_index=True)

# ==============================
# 4. CLEAN TEXT (VERY IMPORTANT)
# ==============================

def clean_text(text):
    return (
        str(text)
        .strip()
        .upper()
        .replace("/", "_")
        .replace("-", "_")
        .replace("  ", " ")
    )

dengue_long["District"] = dengue_long["District"].apply(clean_text)
dengue_long["MOH"] = dengue_long["MOH"].apply(clean_text)
dengue_long["Week"] = dengue_long["Week"].astype(str).str.strip()

# ==============================
# 5. KEEP FINAL REQUIRED COLUMNS
# ==============================

final_dengue = dengue_long[
    ["District", "MOH", "Year", "Week", "Dengue_Cases"]
]

# ==============================
# 6. SAVE OUTPUT
# ==============================

final_dengue.to_csv(
    "dengue_cases_moh_weekly_2013_2022.csv",
    index=False
)

print("✅ Dengue data successfully converted and saved!")
print(final_dengue.head())
