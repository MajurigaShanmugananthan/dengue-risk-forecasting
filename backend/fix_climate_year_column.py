import pandas as pd

input_file = r"E:\dengue_project\data\processed\weekly_climate_data_2013_2022.xlsx"
output_file = r"E:\dengue_project\data\processed\weekly_climate_data_fixed.xlsx"

df = pd.read_excel(input_file)

df.columns = df.columns.str.strip()
df.rename(columns={'week': 'Week'}, inplace=True)

print("📂 Original climate file columns:", df.columns.tolist())

# ---- Identify how many weeks per MOH ----
# climate file contains: for each MOH, 2013→2022 data
# so for each MOH, sort, split into 10 equal parts
df = df.sort_values(["District", "MOH", "Week"]).reset_index(drop=True)

mohs = df["MOH"].unique()
years = list(range(2013, 2023))

df["Year"] = None

for moh in mohs:
    part = df[df["MOH"] == moh]
    n = len(part)

    # total rows should divide by 10 years
    rows_per_year = n // len(years)

    year_values = []
    idx = 0
    for yr in years:
        year_values.extend([yr] * rows_per_year)
        idx += rows_per_year

    # If some extra rows remain (rare due to week 53)
    if len(year_values) < n:
        extra = n - len(year_values)
        year_values.extend([2022] * extra)

    df.loc[df["MOH"] == moh, "Year"] = year_values

df["Year"] = df["Year"].astype(int)

print("✅ Year column inserted")

df.to_excel(output_file, index=False)
print("💾 Saved:", output_file)
