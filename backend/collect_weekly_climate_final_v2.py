# E:\dengue_project\backend\collect_weekly_climate_final_v2.py
import pandas as pd
from meteostat import Point, Daily, Stations
from datetime import datetime
import os, time

# --- File paths ---
moh_file = r"E:\dengue_project\data\raw\moh_with_coordinates.xlsx"
output_file = r"E:\dengue_project\data\processed\weekly_climate_data_2013_2022.xlsx"
checkpoint_file = r"E:\dengue_project\data\processed\_completed_mohs.txt"

# --- Settings ---
start = datetime(2013, 1, 1)
end = datetime(2022, 12, 31)
delay_seconds = 2
batch_size = 20

# --- Load MOH coordinates ---
moh_df = pd.read_excel(moh_file)
moh_df.columns = ['District', 'Admin Area', 'MOH', 'Latitude', 'Longitude']

# --- Resume progress ---
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, "r") as f:
        completed_mohs = set(line.strip() for line in f.readlines())
else:
    completed_mohs = set()

remaining_mohs = [row for _, row in moh_df.iterrows() if row['MOH'] not in completed_mohs]
print(f"🔄 Resuming... {len(remaining_mohs)} MOHs remaining to collect climate data")

# --- Function: Save partial results safely ---
def save_partial(df):
    if not os.path.exists(output_file):
        df.to_excel(output_file, index=False)
    else:
        existing = pd.read_excel(output_file)
        combined = pd.concat([existing, df], ignore_index=True)
        combined.drop_duplicates(subset=["MOH", "week"], inplace=True)
        combined.to_excel(output_file, index=False)

# --- Function: Get nearest available station if no data ---
def get_nearest_station(lat, lon, radius_km=50):
    stations = Stations().nearby(lat, lon)
    nearby = stations.fetch(limit=1)
    if nearby.empty:
        return None
    station = nearby.iloc[0]
    return Point(station['latitude'], station['longitude'])

# --- Main loop ---
for i in range(0, len(remaining_mohs), batch_size):
    batch = remaining_mohs[i:i + batch_size]
    batch_results = []

    for _, row in enumerate(batch):
        moh_name = row['MOH']
        lat, lon = row['Latitude'], row['Longitude']

        if pd.isna(lat) or pd.isna(lon):
            print(f"⚠️ Skipping {moh_name}: missing coordinates")
            continue

        print(f"📍 Fetching data for {moh_name} ({lat}, {lon})...")

        try:
            location = Point(lat, lon)
            data = Daily(location, start, end).fetch()

            # If empty, use nearest weather station
            if data.empty:
                print(f"❗ No direct data for {moh_name}, trying nearest station...")
                nearest = get_nearest_station(lat, lon)
                if nearest:
                    data = Daily(nearest, start, end).fetch()
                    if data.empty:
                        print(f"❌ Still no data found for {moh_name}")
                        continue
                else:
                    print(f"🚫 No nearby station found for {moh_name}")
                    continue

            # Compute weekly averages
            columns = ['tavg', 'tmin', 'tmax', 'prcp', 'wspd']
            if 'rhum' in data.columns:
                columns.append('rhum')

            data['week'] = data.index.to_period('W').start_time
            weekly = data.groupby('week')[columns].mean().reset_index()

            weekly['MOH'] = moh_name
            weekly['District'] = row['District']
            weekly['Latitude'] = lat
            weekly['Longitude'] = lon

            batch_results.append(weekly)

            # Mark as completed
            with open(checkpoint_file, "a") as f:
                f.write(f"{moh_name}\n")

            print(f"✅ Completed: {moh_name}")
            time.sleep(delay_seconds)

        except Exception as e:
            print(f"⚠️ Error for {moh_name}: {e}")
            continue

    # Save progress after each batch
    if batch_results:
        df_batch = pd.concat(batch_results, ignore_index=True)
        save_partial(df_batch)
        print(f"💾 Batch {i // batch_size + 1} saved ({len(batch_results)} MOHs).")

print("🎉 Climate data collection finished for all MOHs!")
