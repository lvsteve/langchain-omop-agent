import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
from agents.summarizer_agent import summarize

# Load environment variables
load_dotenv()

# Create a database engine
engine = create_engine(os.getenv("DATABASE_URI"))

def test_diabetes_hypertension():
    # First get all patients with diabetes
    diabetes_id = 201826  # Type 2 diabetes mellitus
    hypertension_ids = [320128, 319826, 319825, 319827, 319828]
    hypertension_ids_str = ','.join(map(str, hypertension_ids))
    
    query = f"""
    WITH diabetes_patients AS (
        SELECT DISTINCT person_id
        FROM cdm.condition_occurrence
        WHERE condition_concept_id = {diabetes_id}
    ),
    hypertension_patients AS (
        SELECT DISTINCT person_id
        FROM cdm.condition_occurrence
        WHERE condition_concept_id IN ({hypertension_ids_str})
    ),
    combined_patients AS (
        SELECT d.person_id
        FROM diabetes_patients d
        INNER JOIN hypertension_patients h ON d.person_id = h.person_id
    ),
    yearly_data AS (
        SELECT 
            EXTRACT(YEAR FROM co.condition_start_date) as visit_year,
            p.person_id
        FROM combined_patients p
        INNER JOIN cdm.condition_occurrence co ON p.person_id = co.person_id
        WHERE co.condition_concept_id IN ({diabetes_id}, {hypertension_ids_str})
        AND EXTRACT(YEAR FROM co.condition_start_date) >= 2016
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
        print("\nDiabetes and Hypertension by Year (2016-Present):")
        print(summarize(result))

if __name__ == "__main__":
    test_diabetes_hypertension() 