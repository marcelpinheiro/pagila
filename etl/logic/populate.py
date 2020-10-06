import sys
from pathlib import Path
sys.path.append(str((Path(__file__).parent/"../").resolve()))
from sqlalchemy.exc import IntegrityError
import logic.session as session

source_session = session.pagila()
destination_session = session.producao()

def populate_actor():
    from sources.actor import Actor    

    query = source_session.query(Actor.first_name, Actor.last_name, Actor.last_update)

    for row in query:     
        rows = Actor(first_name=row.first_name,last_name=row.last_name,last_update=row.last_update)
        destination_session.add(rows)
    destination_session.commit() 


def populate_film():
    from sources.film import Film    

    query = source_session.query(Film.title, Film.description, Film.release_year, Film.last_update)

    for row in query:     
        rows = Film(title=row.title,description=row.description,release_year=row.release_year,last_update=row.last_update)
        destination_session.add(rows)
    destination_session.commit() 


def populate_city():
    from sources.city import City    

    query = source_session.query(City.city)

    for row in query:     
        rows = City(city=row.city)
        destination_session.add(rows)
    destination_session.commit() 

source_session.close()
destination_session.close()   