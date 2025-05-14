import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
from agents.summarizer_agent import summarize

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URI"))

# Test with hospitalization data
query = '''
SELECT 
    EXTRACT(YEAR FROM visit_start_date) as year,
    CASE visit_concept_id
        WHEN 9201 THEN 'Inpatient'
        WHEN 9203 THEN 'ER'
        WHEN 262 THEN 'ER+Inpatient'
    END AS visit_type,
    COUNT(DISTINCT person_id) as patients,
    COUNT(*) as total_visits
FROM cdm.visit_occurrence
WHERE visit_concept_id IN (9201, 9203, 262)
    AND EXTRACT(YEAR FROM visit_start_date) >= 2016
GROUP BY 
    EXTRACT(YEAR FROM visit_start_date),
    visit_concept_id
ORDER BY 
    year,
    visit_type;
'''

with engine.connect() as conn:
    result = conn.execute(text(query))
    # Convert to DataFrame
    df = pd.DataFrame(result.fetchall(), columns=['year', 'visit_type', 'patients', 'total_visits'])
    
    print("\n=== Summarizer Agent Test ===")
    print("Input: Hospitalization data by year and type")
    print("\nRaw data:")
    for _, row in df.iterrows():
        print(f"Year: {int(row['year'])}, Type: {row['visit_type']}, Patients: {row['patients']}, Visits: {row['total_visits']}")
    
    print("\nSummarizer output:")
    print(summarize(df)) 