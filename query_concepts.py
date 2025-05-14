import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URI"))

query = '''
SELECT concept_id, concept_name
FROM cdm.concept
WHERE domain_id = 'Condition'
  AND (
    concept_name ILIKE '%type 1 diabetes%' 
    OR concept_name ILIKE '%type i diabetes%'
    OR concept_name ILIKE '%type 2 diabetes%'
    OR concept_name ILIKE '%type ii diabetes%'
    OR concept_name ILIKE '%essential hypertension%'
  )
ORDER BY concept_name;
'''

with engine.connect() as conn:
    result = conn.execute(text(query))
    for row in result:
        print(row) 