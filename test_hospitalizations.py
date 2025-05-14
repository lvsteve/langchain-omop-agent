import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
from agents.summarizer_agent import summarize

# Load environment variables
load_dotenv()

# Create a database engine
engine = create_engine(os.getenv("DATABASE_URI"))

def test_hospitalizations():
    query = """
    WITH filtered_visits AS (
        SELECT DISTINCT vo.person_id, vo.visit_occurrence_id
        FROM cdm.visit_occurrence vo
        WHERE EXTRACT(YEAR FROM vo.visit_start_date) >= 2016
        AND vo.visit_concept_id = 9201
    )
    SELECT 
        EXTRACT(YEAR FROM vo.visit_start_date) as visit_year,
        COUNT(DISTINCT vo.person_id) as patient_count,
        COUNT(DISTINCT vo.visit_occurrence_id) as record_count
    FROM filtered_visits fv
    JOIN cdm.visit_occurrence vo ON fv.visit_occurrence_id = vo.visit_occurrence_id
    GROUP BY EXTRACT(YEAR FROM vo.visit_start_date)
    ORDER BY visit_year
    """
    
    with engine.connect() as conn:
        result = pd.read_sql(query, conn)
        print("\nHospitalizations by Year (2016-Present):")
        print(summarize(result))

if __name__ == "__main__":
    test_hospitalizations() 