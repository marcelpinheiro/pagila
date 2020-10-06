import sys
from pathlib import Path
sys.path.append(str((Path(__file__).parent/"../").resolve()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, select, func

Base = declarative_base()
class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key = True)
    city = Column(String(100))