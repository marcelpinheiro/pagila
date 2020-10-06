import sys
from pathlib import Path
sys.path.append(str((Path(__file__).parent/"../").resolve()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, select, func

Base = declarative_base()

class Film(Base):
    __tablename__ = 'film'  
    
    film_id = Column(Integer, primary_key = True)
    title = Column(String(50))
    description = Column(String(250))
    release_year = Column(Integer)
    last_update = Column(DateTime)
