import pandas as pd

input_file = r"E:\dengue_project\data\processed\weekly_climate_data_2013_2022.xlsx"
output_file = r"E:\dengue_project\data\processed\weekly_climate_data_fixed.xlsx"

print("📂 Loading climate file...")
df = pd.read_excel(input_file)

# Standardize column names
df.columns = df.columns.str.strip()
df.rename(columns={"week": "Week"}, inplace=True)

# Sort by District, MOH, Week to ensure correct ordering
df = df.sort_values(["District", "MOH", "Week"]).reset_index(drop=True)

years = list(range(2013, 2023))  # 2013–2022

print("📅 Adding Year column...")

# ---- Logic ----
# For each MOH:
#   Count how many rows per year = number of weeks for that year
#   Assign Year sequentially
df["Year"] = None

for moh in df["MOH"].unique():
    moh_df = df[df["MOH"] == moh]
    years_cycle = []

    # Repeat years 2013–2022 for each MOH
    for year in years:
        weeks_in_year = len(moh_df[moh_df["Week"].between(1, 53)])

        # append repeated rows
        years_cycle.extend([year] * weeks_in_year)

    # Assign back
    df.loc[df["MOH"] == moh, "Year"] = years_cycle[:len(moh_df)]

df["Year"] = df["Year"].astype(int)

print("💾 Saving file with Year column...")
df.to_excel(output_file, index=False)

print("\n✅ Climate file fixed and saved as:", output_file)
