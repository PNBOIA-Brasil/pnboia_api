# Import all the models, so that Base has them before being
# imported by Alembic
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  

from dotenv import load_dotenv

load_dotenv()

def engine_create(qc=True):

    if qc:
        password = os.getenv('REMOBS_QC_DB_PASSWORD')
        local = os.getenv('REMOBS_QC_DB_URL')
        engine = create_engine(f"postgresql+psycopg2://{os.getenv('REMOBS_QC_DB_USR')}:{quote(password)}@{local}/{os.getenv('REMOBS_QC_DB')}")

    return engine

engine = engine_create()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


