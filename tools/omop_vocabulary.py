from tools.db_connection import get_connection
from sqlalchemy import text

def lookup_concepts(term):
    """
    Look up concept IDs for a given medical term.
    Handles partial matches and multiple terms.
    
    Args:
        term (str): Medical term to look up (e.g., "type 1 diabetes", "essential hypertension")
    
    Returns:
        list: List of concept IDs matching the term
    """
    # Split the term into words and create a pattern
    words = term.lower().split()
    pattern = ' AND '.join([f"lower(concept_name) LIKE '%{word}%'" for word in words])
    
    sql = f"""
    SELECT concept_id, concept_name 
    FROM cdm.concept
    WHERE {pattern}
    AND domain_id = 'Condition'
    ORDER BY 
        CASE 
            WHEN lower(concept_name) = lower('{term}') THEN 1
            WHEN lower(concept_name) LIKE lower('%{term}%') THEN 2
            ELSE 3
        END,
        concept_name
    LIMIT 5
    """
    
    with get_connection() as conn:
        result = conn.execute(text(sql))
        concepts = [(row[0], row[1]) for row in result]
        if concepts:
            print(f"Found concepts for '{term}':")
            for concept_id, concept_name in concepts:
                print(f"  - {concept_name} (ID: {concept_id})")
        return [concept[0] for concept in concepts]
