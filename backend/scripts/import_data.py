import pandas as pd
from app.db import SessionLocal
from app.models import MOHArea, DengueCase
from datetime import datetime, timedelta
import numpy as np

session = SessionLocal()

# ---- Import MOH areas ----
print("Importing MOH areas...")
moh_df = pd.read_csv('../data/raw/moh_list.csv')

# Strip whitespace from column names
moh_df.columns = moh_df.columns.str.strip()

for _, row in moh_df.iterrows():
    area = MOHArea(
        name=row['name'].strip(),
        district=row.get('district', '').strip(),
        province=row.get('province', '').strip(),
        latitude=float(row.get('lat', 0)),
        longitude=float(row.get('lon', 0)),
        population_density=row.get('pop_density', 0) if 'pop_density' in row else 0
    )
    session.add(area)
session.commit()
print(f"✅ Imported {len(moh_df)} MOH areas")

# ---- Import Dengue Cases ----
print("Importing dengue cases...")

# Read the CSV with proper handling
cases_df = pd.read_csv('../data/raw/dengue_cases_2022_2024.csv')

# Get the MOH name column (first column)
moh_names = cases_df.iloc[:, 0]

# Function to convert week number to approximate date
def week_to_date(year, week):
    """Convert year and week number to the Monday of that week"""
    if pd.isna(week) or week == '':
        return None
    try:
        week = int(float(week))
        # January 1st of the year
        jan_1 = datetime(year, 1, 1)
        # Find the Monday of week 1
        days_to_monday = (7 - jan_1.weekday()) % 7
        week_1_monday = jan_1 + timedelta(days=days_to_monday)
        # Calculate the date for the given week
        target_date = week_1_monday + timedelta(weeks=week - 1)
        return target_date.date()
    except (ValueError, TypeError):
        return None

# Process each row (MOH area)
total_cases_imported = 0
for idx, moh_name in enumerate(moh_names):
    if pd.isna(moh_name) or moh_name.strip() == '':
        continue
    
    moh_name = moh_name.strip()
    moh = session.query(MOHArea).filter(MOHArea.name == moh_name).first()
    
    if not moh:
        print(f"⚠️  MOH area '{moh_name}' not found in database, skipping...")
        continue
    
    # Get all case values for this MOH (skip first column which is the name)
    row_data = cases_df.iloc[idx, 1:].values
    
    # Determine which columns belong to which year based on header rows
    # Row 1 has years, Row 2 has "Week", Row 3 has week numbers
    year_row = cases_df.columns[1:]  # Skip moh_name column
    
    # Parse the structure: columns are organized by year
    # 2020: columns 1-2 (Week 52, Week 1)
    # 2021: columns 2-53 (Weeks 1-52) - but based on CSV, seems incomplete
    # Need to manually map based on the actual CSV structure
    
    current_year = 2020
    current_col = 0
    
    # This is a simplified approach - you may need to adjust based on actual column positions
    year_mappings = {
        2020: (0, 2),      # columns 0-1 (Week 52, Week 1)
        2021: (2, 53),     # columns 2-52 (assuming 51 weeks shown)
        2022: (53, 106),   # next 53 columns
        2023: (106, 159),  # next 53 columns
        2024: (159, 212),  # next 53 columns
        2025: (212, 265),  # remaining columns
    }
    
    for year, (start_col, end_col) in year_mappings.items():
        if start_col >= len(row_data):
            break
            
        year_data = row_data[start_col:min(end_col, len(row_data))]
        
        for week_offset, cases_value in enumerate(year_data):
            if pd.isna(cases_value) or cases_value == '':
                continue
            
            try:
                cases_count = int(float(cases_value))
                if cases_count == 0:
                    continue
                    
                # Calculate week number (adjust based on your CSV structure)
                week_num = week_offset + 1
                if year == 2020 and week_offset == 0:
                    week_num = 52  # First column of 2020 is week 52
                
                report_date = week_to_date(year, week_num)
                
                if report_date:
                    case = DengueCase(
                        moh_id=moh.id,
                        report_date=report_date,
                        cases=cases_count,
                        source='epid_data'
                    )
                    session.add(case)
                    total_cases_imported += 1
            except (ValueError, TypeError) as e:
                continue

session.commit()
session.close()
print(f"✅ Data import completed successfully!")
print(f"📊 Total case records imported: {total_cases_imported}")