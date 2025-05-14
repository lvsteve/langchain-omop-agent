import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a database engine
engine = create_engine(os.getenv("DATABASE_URI"))

# Test the connection and query for concept IDs
try:
    with engine.connect() as connection:
        # Verify Type I diabetes concept ID
        result = connection.execute(text("SELECT concept_name FROM cdm.concept WHERE concept_id = 40353858"))
        concept_name = result.scalar()
        print("Type I diabetes concept name:", concept_name)

        # Verify Type II diabetes concept ID
        result = connection.execute(text("SELECT concept_name FROM cdm.concept WHERE concept_id = 40353859"))
        concept_name = result.scalar()
        print("Type II diabetes concept name:", concept_name)

except Exception as e:
    print(f"Database connection or query failed: {e}") 