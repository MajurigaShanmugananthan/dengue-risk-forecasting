# prepare_climate_weekly.py
import pandas as pd
import os

INPUT = r"E:\dengue_project\data\processed\weekly_climate_data_2013_2022.xlsx"
OUTPUT = r"E:\dengue_project\data\processed\weekly_climate_data_prepared.xlsx"

print("Loading climate file...")
df = pd.read_excel(INPUT)

# Standardize column names
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Identify week column (date)
if "week" in df.columns:
    wk_col = "week"
elif "Week" in df.columns:
    wk_col = "Week"
else:
    raise SystemExit("No 'week' or 'Week' column found in climate file.")

# ❗ Remove any existing Week column to avoid conflicts later
if "Week" in df.columns and wk_col != "Week":
    df = df.drop(columns=["Week"])

# Convert week column to datetime
df[wk_col] = pd.to_datetime(df[wk_col], errors="coerce")

# Drop invalid dates
df = df.dropna(subset=[wk_col])

# Extract ISO calendar info
iso = df[wk_col].dt.isocalendar()
df["Year"] = iso["year"].astype(int)
df["Week"] = iso["week"].astype(int)

# Clean string columns
for col in ["District", "MOH"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# Aggregation mapping
agg_map = {}
for c in df.select_dtypes(include="number").columns:
    if c.lower().startswith("pr"):  
        agg_map[c] = "sum"     # precipitation
    else:
        agg_map[c] = "mean"    # temperatures, wind

for c in ["Latitude", "Longitude"]:
    if c in df.columns:
        agg_map[c] = "first"

# Group & aggregate
group_cols = ["District", "MOH", "Year", "Week"]
print("Aggregating climate by", group_cols)

clim_weekly = (
    df.groupby(group_cols)
      .agg(agg_map)
      .reset_index()
)

# Save
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
clim_weekly.to_excel(OUTPUT, index=False)

print("✅ Climate weekly file saved:", OUTPUT)
print("📊 Total rows:", len(clim_weekly))
