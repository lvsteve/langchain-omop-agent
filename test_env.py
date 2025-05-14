import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Print current working directory
print("Current working directory:", os.getcwd())

# Print .env file path
env_path = pathlib.Path('.env')
print(".env file exists:", env_path.exists())
print(".env file absolute path:", env_path.absolute())

# Try to load .env file
load_dotenv()

# Print all environment variables (filtered for security)
print("\nEnvironment variables:")
for key, value in os.environ.items():
    if 'DATABASE' in key:
        print(f"{key}: {value}")

print("\nDATABASE_URI:", os.getenv("DATABASE_URI"))

engine = create_engine(os.getenv("DATABASE_URI"))

query = '''
SELECT concept_id, concept_name
FROM cdm.concept
WHERE domain_id = 'Condition'
  AND (concept_name ILIKE '%diabetes%' OR concept_name ILIKE '%hypertension%')
LIMIT 20;
'''

with engine.connect() as conn:
    result = conn.execute(text(query))
    for row in result:
        print(row) 