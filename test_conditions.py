import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
from tools.db_connection import get_connection

# Load environment variables
load_dotenv()

# Create a database engine
engine = create_engine(os.getenv("DATABASE_URI"))

def test_condition(condition_name, concept_ids):
    """Test a specific condition using concept IDs"""
    conn = get_connection()
    
    # Build the query
    concept_ids_str = ','.join(map(str, concept_ids))
    query = f"""
    SELECT COUNT(DISTINCT p.person_id) as patient_count
    FROM cdm.person p
    JOIN cdm.condition_occurrence co ON p.person_id = co.person_id
    WHERE co.condition_concept_id IN ({concept_ids_str})
    """
    
    # Execute query
    result = pd.read_sql(query, conn)
    print(f"\n{condition_name}:")
    print(f"Found {result['patient_count'].iloc[0]} patients")
    
    return result['patient_count'].iloc[0]

def test_specific_diabetes_conditions():
    # Only use these three concept IDs
    diabetes_ids = [201826, 201254, 443238]
    labels = {}
    with engine.connect() as conn:
        # Fetch concept names for these IDs
        query = f"""
        SELECT concept_id, concept_name FROM cdm.concept WHERE concept_id IN ({','.join(map(str, diabetes_ids))})
        """
        df = pd.read_sql(query, conn.connection)
        for row in df.itertuples():
            labels[row.concept_id] = row.concept_name
    # Count unique patients for each
    for cid in diabetes_ids:
        test_condition(labels.get(cid, f"Concept {cid}"), [cid])

def test_diabetes_age_groups():
    # Use the concept ID for Type 2 diabetes mellitus
    diabetes_id = 201826
    with engine.connect() as conn:
        query = f"""
        SELECT p.person_id, p.year_of_birth, EXTRACT(YEAR FROM CURRENT_DATE) - p.year_of_birth as age
        FROM cdm.person p
        JOIN cdm.condition_occurrence co ON p.person_id = co.person_id
        WHERE co.condition_concept_id = {diabetes_id}
        """
        df = pd.read_sql(query, conn.connection)
    
    # Define age groups
    bins = [0, 18, 30, 50, 70, float('inf')]
    labels = ['0-18', '19-30', '31-50', '51-70', '70+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
    
    # Count patients in each age group
    age_group_counts = df['age_group'].value_counts().sort_index()
    print("\nPatients with Type 2 Diabetes Mellitus by Age Group:")
    for age_group, count in age_group_counts.items():
        print(f"{age_group}: {count} patients")

def count_patients_by_condition():
    diabetes_ids = [201826, 201254, 443238]
    hypertension_ids = [320128, 319826, 319825, 319827, 319828]
    with engine.connect() as conn:
        # Diabetes
        diabetes_query = f"""
        SELECT COUNT(DISTINCT p.person_id) as patient_count
        FROM cdm.person p
        JOIN cdm.condition_occurrence co ON p.person_id = co.person_id
        WHERE co.condition_concept_id IN ({','.join(map(str, diabetes_ids))})
        """
        diabetes_count = pd.read_sql(diabetes_query, conn.connection)['patient_count'].iloc[0]
        print(f"\nTotal unique patients with diabetes: {diabetes_count}")
        # Hypertension
        hypertension_query = f"""
        SELECT COUNT(DISTINCT p.person_id) as patient_count
        FROM cdm.person p
        JOIN cdm.condition_occurrence co ON p.person_id = co.person_id
        WHERE co.condition_concept_id IN ({','.join(map(str, hypertension_ids))})
        """
        hypertension_count = pd.read_sql(hypertension_query, conn.connection)['patient_count'].iloc[0]
        print(f"Total unique patients with hypertension: {hypertension_count}")

def main():
    # Test essential hypertension
    hypertension_ids = [320128, 319826, 319825, 319827, 319828]
    test_condition("Essential Hypertension", hypertension_ids)
    
    # Test only the three specific diabetes codes
    test_specific_diabetes_conditions()
    
    # Test diabetes age groups
    test_diabetes_age_groups()
    
    # Count unique patients with diabetes and hypertension
    count_patients_by_condition()

if __name__ == "__main__":
    main()

# Test the connection and query for conditions
try:
    with engine.connect() as connection:
        # Test for hospitalizations since 2020
        result = connection.execute(text("SELECT COUNT(*) FROM cdm.visit_occurrence WHERE visit_concept_id = 9201 AND EXTRACT(YEAR FROM visit_start_date) >= 2020"))
        print("Number of hospitalizations since 2020:", result.scalar())

        # Test for ER visits since 2020
        result = connection.execute(text("SELECT COUNT(*) FROM cdm.visit_occurrence WHERE visit_concept_id = 9203 AND EXTRACT(YEAR FROM visit_start_date) >= 2020"))
        print("Number of ER visits since 2020:", result.scalar())

except Exception as e:
    print(f"Database connection or query failed: {e}") 