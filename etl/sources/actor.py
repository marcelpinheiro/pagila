from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actor'
    
    KEY_COLUMNS = ('actor_id',)
    ETL_COLUMNS = ('actor_id','first_name','last_name','last_update')

    actor_id = Column(Integer, primary_key = True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    last_update = Column(DateTime)



