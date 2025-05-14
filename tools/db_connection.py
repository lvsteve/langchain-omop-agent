import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("OMOP_DB_URI"))

def get_connection():
    return engine.connect()
