import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
from agents.summarizer_agent import summarize

# Load environment variables
load_dotenv()

# Create a database engine
engine = create_engine(os.getenv("DATABASE_URI"))

def test_diabetes():
    diabetes_id = 201826  # Type 2 diabetes mellitus
    
    query = f"""
    WITH yearly_data AS (
        SELECT 
            EXTRACT(YEAR FROM condition_start_date) as visit_year,
            person_id
        FROM cdm.condition_occurrence
        WHERE condition_concept_id = {diabetes_id}
        AND EXTRACT(YEAR FROM condition_start_date) >= 2016
    )
    SELECT 
        visit_year,
        COUNT(DISTINCT person_id) as patient_count,
        COUNT(DISTINCT person_id) as record_count
    FROM yearly_data
    GROUP BY visit_year
    ORDER BY visit_year
    """
    
    with engine.connect() as conn:
        result = pd.read_sql(query, conn)
        print("\nDiabetes by Year (2016-Present):")
        print(summarize(result))

if __name__ == "__main__":
    test_diabetes() 