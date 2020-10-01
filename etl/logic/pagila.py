import sys
from pathlib import Path
sys.path.append(str((Path(__file__).parent/"../../").resolve()))
from sqlalchemy.exc import IntegrityError
from .etl_base import sync


def run_actor(source_session, target_session):
    
    from etl.sources.actor import Actor as Source
    from etl.targets import Actor as Target
        
    sync(source_session, Source, target_session, Target)        
