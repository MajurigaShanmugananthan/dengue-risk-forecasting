import pandas as pd
from datetime import datetime
from app.db import SessionLocal
from app.models import MOHArea, DengueCase, ClimateRecord

session = SessionLocal()

# --- 1️⃣ Import MOH areas ---
print("Importing MOH areas...")
moh_df = pd.read_csv('../data/raw/moh_list.csv')
session.query(MOHArea).delete()  # clear existing
session.commit()

for _, row in moh_df.iterrows():
    moh = MOHArea(
        name=row['name'],
        district=row.get('district'),
        province=row.get('province'),
        latitude=float(row['lat']),
        longitude=float(row['lon']),
        population_density=int(row.get('pop_density', 0))
    )
    session.add(moh)
session.commit()
print(f"Inserted {len(moh_df)} MOH areas.")

# --- 2️⃣ Import Dengue cases ---
print("Importing dengue cases...")
cases_df = pd.read_csv('../data/raw/dengue_cases_2022_2024.csv')
session.query(DengueCase).delete()
session.commit()

for _, row in cases_df.iterrows():
    moh = session.query(MOHArea).filter(MOHArea.name == row['moh_name']).first()
    if moh:
        case = DengueCase(
            moh_id=moh.id,
            report_date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
            cases=int(row['cases']),
            source='real_data'
        )
        session.add(case)
session.commit()
print(f"Inserted {len(cases_df)} dengue case records.")

# --- 3️⃣ Import Climate data ---
print("Importing climate data...")
climate_df = pd.read_csv('../data/raw/climate_2022_2024.csv')
session.query(ClimateRecord).delete()
session.commit()

for _, row in climate_df.iterrows():
    moh = session.query(MOHArea).filter(MOHArea.name == row['moh_name']).first()
    if moh:
        record = ClimateRecord(
            moh_id=moh.id,
            date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
            rainfall=float(row['rainfall']),
            temperature=float(row['temperature']),
            humidity=float(row['humidity'])
        )
        session.add(record)
session.commit()
print(f"Inserted {len(climate_df)} climate records.")

session.close()
print("✅ Real data successfully imported into database.")
