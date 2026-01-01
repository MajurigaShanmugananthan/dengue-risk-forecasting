import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Example: read dengue cases table
cases = pd.read_sql("SELECT * FROM dengue_cases", engine, parse_dates=['report_date'])
climate = pd.read_sql("SELECT * FROM climate_data", engine, parse_dates=['date'])
moh = pd.read_sql("SELECT * FROM moh_areas", engine)

# basic aggregation: weekly cases per moh
cases['week'] = cases['report_date'].dt.to_period('W').apply(lambda r: r.start_time)
weekly = cases.groupby(['moh_id','week']).cases.sum().reset_index()
# merge with climate weekly averages
climate['week'] = climate['date'].dt.to_period('W').apply(lambda r: r.start_time)
climate_weekly = climate.groupby(['moh_id','week']).agg({'rainfall':'mean','temperature':'mean'}).reset_index()

df = weekly.merge(climate_weekly, on=['moh_id','week'], how='left')
df = df.fillna(0)
df.to_csv('../data/processed/weekly_features.csv', index=False)
print("Prepared weekly data:", df.shape)
