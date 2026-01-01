# app/models.py
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MOHArea(Base):
    __tablename__ = 'moh_areas'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    district = Column(String)
    province = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    population_density = Column(Integer)

class DengueCase(Base):
    __tablename__ = 'dengue_cases'
    id = Column(Integer, primary_key=True)
    moh_id = Column(Integer, ForeignKey('moh_areas.id'), nullable=False)
    report_date = Column(Date, nullable=False)
    cases = Column(Integer, nullable=False)
    source = Column(String)
    moh = relationship("MOHArea")

class ClimateRecord(Base):
    __tablename__ = 'climate_data'
    id = Column(Integer, primary_key=True)
    moh_id = Column(Integer, ForeignKey('moh_areas.id'))
    date = Column(Date)
    rainfall = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    moh = relationship("MOHArea")

class SocialSignal(Base):
    __tablename__ = 'social_signals'
    id = Column(Integer, primary_key=True)
    moh_id = Column(Integer, ForeignKey('moh_areas.id'))
    date = Column(Date)
    mentions = Column(Integer)
    source = Column(String)
    moh = relationship("MOHArea")
