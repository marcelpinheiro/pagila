import sys
from pathlib import Path
sys.path.append(str((Path(__file__).parent/"../").resolve()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, select, func

Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actor'
    
    actor_id = Column(Integer, primary_key = True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    last_update = Column(DateTime)
