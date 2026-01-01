import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

def clean_name(text):
    if pd.isna(text):
        return text
    text = text.lower()
    text = re.sub(r"[()]", "", text)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().title()

files = {
    "dengue": BASE_DIR / "data/processed/dengue_cases_weekly_long.csv",
    "climate": BASE_DIR / "data/processed/weekly_climate_new_moh.csv",
}

for name, path in files.items():
    df = pd.read_csv(path)
    df["District"] = df["District"].apply(clean_name)
    df["MOH"] = df["MOH"].apply(clean_name)
    df.to_csv(BASE_DIR / f"data/processed/{name}_names_clean.csv", index=False)

print("✅ MOH & District names standardized")
