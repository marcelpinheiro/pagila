from etl.logic import pagila
import argparse
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


CONFIG_SESSIONS = {
    'actor': {
        'logic': pagila.run_actor,
        'source': session_pagila,
        'target': session_producao,
    }
}


if __name__ == '__main__':
    
    print('== INIT ==')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=CONFIG_SESSIONS.keys())
    args = parser.parse_args()
    
    
    config_key = args.task
    
    config_value = CONFIG_SESSIONS[config_key]
    
    logic = config_value['logic']
    source = config_value['source']
    target = config_value['target']
    
    logic(source, target)
    
    print('== END ==')

