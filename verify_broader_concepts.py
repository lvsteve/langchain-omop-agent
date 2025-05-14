import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a database engine
engine = create_engine(os.getenv("DATABASE_URI"))

# Test the connection and query for broader diabetes concepts
try:
    with engine.connect() as connection:
        # Query for broader diabetes concepts
        result = connection.execute(text("SELECT concept_id, concept_name FROM cdm.concept WHERE concept_name LIKE '%diabetes%'"))
        concepts = result.fetchall()
        print("Broader diabetes concepts:")
        for concept_id, concept_name in concepts:
            print(f"Concept ID: {concept_id}, Concept Name: {concept_name}")

except Exception as e:
    print(f"Database connection or query failed: {e}") 