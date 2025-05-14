import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Create a database engine
engine = create_engine(os.getenv("DATABASE_URI"))

def test_hypertension():
    hypertension_ids = [320128, 319826, 319825, 319827, 319828]
    hypertension_ids_str = ','.join(map(str, hypertension_ids))
    
    query = f"""
    WITH yearly_data AS (
        SELECT 
            EXTRACT(YEAR FROM condition_start_date) as visit_year,
            person_id
        FROM cdm.condition_occurrence
        WHERE condition_concept_id IN ({hypertension_ids_str})
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
        print("\nHypertension by Year (2016-Present):")
        print(result)
        
        # Print total counts
        total_patients = result['patient_count'].sum()
        total_records = result['record_count'].sum()
        print(f"\nTotal unique patients: {total_patients}")
        print(f"Total records: {total_records}")

if __name__ == "__main__":
    test_hypertension() 