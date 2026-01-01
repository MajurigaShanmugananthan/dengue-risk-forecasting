import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

INPUT_DIR = BASE_DIR / "data/raw/climate_daily"
OUTPUT_DIR = BASE_DIR / "data/processed/climate_weekly"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for file in INPUT_DIR.glob("*_daily.csv"):
    df = pd.read_csv(file, index_col=0, parse_dates=True)

    weekly = df.resample("W-MON").agg({
        "T2M": "mean",
        "T2M_MIN": "mean",
        "T2M_MAX": "mean",
        "PRECTOTCORR": "sum",
        "WS2M": "mean",
        "District": "first",
        "MOH": "first",
        "Latitude": "first",
        "Longitude": "first"
    }).reset_index()

    weekly.rename(columns={
        "index": "week",
        "T2M": "tavg",
        "T2M_MIN": "tmin",
        "T2M_MAX": "tmax",
        "PRECTOTCORR": "prcp",
        "WS2M": "wspd"
    }, inplace=True)

    output_name = file.name.replace("_daily.csv", "_weekly.csv")
    weekly.to_csv(OUTPUT_DIR / output_name, index=False)

print("✅ Weekly climate data created.")
