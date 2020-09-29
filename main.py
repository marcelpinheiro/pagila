from sqlalchemy import create_engine
from decouple import config
from sqlalchemy.orm import sessionmaker

#Engines
#Database who has all data (source)
engine_pagila = create_engine(config('PAGILA_DB_AWS_POSTGRES'), echo=True)
#Database with the result of the ETL (target)
engine_producao = create_engine(config('PRODUCAO_DB_AWS_MYSQL'), echo=True)

#Sessions
session_pagila = sessionmaker(bind=engine_pagila)
session_producao = sessionmaker(bind=engine_producao)

