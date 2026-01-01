import pandas as pd
from geopy.geocoders import Nominatim
import time

# Load your Excel file
df = pd.read_excel("E:/dengue_project/data/raw/moh_coordinates.xlsx")

geolocator = Nominatim(user_agent="dengue_moh_locator")

latitudes = []
longitudes = []

for moh in df["MOH"]:
    try:
        location = geolocator.geocode(f"{moh}, Sri Lanka")
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            print(f"{moh} → {location.latitude}, {location.longitude}")
        else:
            latitudes.append(None)
            longitudes.append(None)
            print(f"❌ Not found: {moh}")
        time.sleep(1)  # Prevent API blocking
    except Exception as e:
        print(f"Error for {moh}: {e}")
        latitudes.append(None)
        longitudes.append(None)

df["Latitude"] = latitudes
df["Longitude"] = longitudes

# Save output
df.to_excel("E:/dengue_project/data/raw/moh_with_coordinates.xlsx", index=False)
print("✅ Saved: moh_with_coordinates.xlsx")
