import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
df = pd.read_csv(
    BASE_DIR / "data/processed/fixed_dengue_names_clean.csv",
    parse_dates=["week"]
)

issues = []

for (district, moh), g in df.groupby(["District", "MOH"]):
    weeks = g["week"].sort_values()
    gaps = weeks.diff().dt.days.gt(7)
    if gaps.any():
        issues.append({
            "District": district,
            "MOH": moh,
            "Missing_Weeks": gaps.sum()
        })

report = pd.DataFrame(issues)
report.to_csv(BASE_DIR / "data/processed/week_gap_report.csv", index=False)

print("✅ Week continuity validation completed")
