import pandas as pd
import requests
from pathlib import Path
from utils import clean_filename


# --------------------------------------------------
# Base paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[4]
MOH_FILE = BASE_DIR / "data/reference/colombo_moh_coordinates.csv"
OUTPUT_DIR = BASE_DIR / "data/raw/climate_daily"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Function to fetch DAILY climate data from NASA POWER
# --------------------------------------------------
def fetch_daily_weather(lat, lon, start="20130101", end="20221231"):
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=T2M,T2M_MIN,T2M_MAX,PRECTOTCORR,WS2M"
        f"&community=SB"
        f"&longitude={lon}&latitude={lat}"
        f"&start={start}&end={end}&format=JSON"
    )

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    data = response.json()["properties"]["parameter"]
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index)

    return df


# --------------------------------------------------
# MAIN PROCESS
# --------------------------------------------------
def main():
    moh_df = pd.read_csv(MOH_FILE)

    for i, row in moh_df.iterrows():
        print(f"⬇ Fetching climate data for: {row.District} - {row.MOH}")

        daily = fetch_daily_weather(row.Latitude, row.Longitude)

        # Add metadata
        daily["District"] = row.District
        daily["MOH"] = row.MOH
        daily["Latitude"] = row.Latitude
        daily["Longitude"] = row.Longitude

        # Safe filename
        district = clean_filename(row.District)
        moh = clean_filename(row.MOH)
        file_name = f"{district}_{moh}_daily.csv"

        daily.to_csv(OUTPUT_DIR / file_name)

    print("\n✅ Daily climate data downloaded successfully.")


# --------------------------------------------------
# Script entry point
# --------------------------------------------------
if __name__ == "__main__":
    main()
