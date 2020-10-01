
import sys
from pathlib import Path
sys.path.append(str((Path(__file__).parent/"..").resolve()))

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

from lib.db import get_or_create_and_maybe_update

Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actor'

    actor_id = Column(Integer, primary_key = True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    last_update = Column(DateTime)


class Film(Base):
    __tablename__ = 'film'
    
    KEY_COLUMNS = ('title')
    __table_args__ = (UniqueConstraint(KEY_COLUMNS),)
    
    film_id = Column(Integer, primary_key = True)
    title = Column(String(50))
    description = Column(String(250))
    release_year = Column(Integer)
    last_update = Column(DateTime)
    


class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key = True)
    city = Column(String(100))


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from decouple import config
    engine = create_engine(config('PRODUCAO_DB_AWS_MYSQL'), echo=True)
    Base.metadata.create_all(engine, checkfirst=True)

    