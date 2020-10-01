import sys
from pathlib import Path
sys.path.append(str((Path(__file__).parent/"../").resolve()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, select, func
import logic.sessions as ss

Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actor'
    
    KEY_COLUMNS = ('actor_id',)
    ETL_COLUMNS = ('actor_id','first_name','last_name','last_update')

    actor_id = Column(Integer, primary_key = True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    last_update = Column(DateTime)




# from sqlalchemy import create_engine
# from decouple import config
# from sqlalchemy.orm import sessionmaker
# #Engines
# #Database who has all data (source)
# engine_pagila = create_engine(config('PAGILA_DB_AWS_POSTGRES'), echo=True)
# #Database with the result of the ETL (target)
# engine_producao = create_engine(config('PRODUCAO_DB_AWS_MYSQL'), echo=True)

# #Sessions
# session_pagila = sessionmaker(bind=engine_pagila)
# session_producao = sessionmaker(bind=engine_producao)


# This is the query we want to persist in a new table:
source_session = ss.session_pagila()
query= source_session.query(Actor.first_name, Actor.last_name, Actor.last_update)

# Finally execute the query
destSession = ss.session_producao()

for row in query:  
    rows = Actor(first_name=row.first_name,last_name=row.last_name,last_update=row.last_update)
    destSession.add(rows)

destSession.commit() 
destSession.close()   