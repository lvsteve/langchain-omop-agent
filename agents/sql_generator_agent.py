def generate(resolved):
    """
    Generate SQL query based on resolved concepts and filters.
    
    Args:
        resolved (dict): Dictionary containing:
            - concept_ids: List of concept IDs or None
            - age_filter: Age filter if specified
            - visit_type: Type of visit if specified
            - year: Year filter if specified
    
    Returns:
        str: Generated SQL query
    """
    # If no valid concept IDs, return a query that returns zero rows
    if resolved.get("concept_ids") is None:
        return "SELECT 1 WHERE 1=0 -- No valid concept IDs found"

    # Base query for patient conditions
    condition_query = """
    SELECT DISTINCT p.person_id, p.year_of_birth
    FROM cdm.person p
    INNER JOIN cdm.condition_occurrence co ON p.person_id = co.person_id
    WHERE 1=1
    """
    
    # Add concept IDs filter if present
    if resolved.get("concept_ids"):
        concept_ids = ', '.join(map(str, resolved["concept_ids"]))
        condition_query += f"\nAND co.condition_concept_id IN ({concept_ids})"
    
    # Add age filter if present
    if resolved.get("age_filter"):
        age = resolved["age_filter"].split(">")[1].strip()
        condition_query += f"\nAND p.year_of_birth <= extract(year from current_date) - {age}"
    
    # If visit type is specified, modify query to include visit information
    if resolved.get("visit_type"):
        visit_type_map = {
            "ER": 9203,
            "Inpatient": 9201
        }
        visit_concept_id = visit_type_map.get(resolved["visit_type"])
        if visit_concept_id:
            condition_query = f"""
            SELECT DISTINCT p.person_id, p.year_of_birth, 
                   COUNT(v.visit_occurrence_id) as visit_count
            FROM cdm.person p
            INNER JOIN cdm.condition_occurrence co ON p.person_id = co.person_id
            INNER JOIN cdm.visit_occurrence v ON p.person_id = v.person_id
            WHERE 1=1
            """
            if resolved.get("concept_ids"):
                concept_ids = ', '.join(map(str, resolved["concept_ids"]))
                condition_query += f"\nAND co.condition_concept_id IN ({concept_ids})"
            if resolved.get("age_filter"):
                age = resolved["age_filter"].split(">")[1].strip()
                condition_query += f"\nAND p.year_of_birth <= extract(year from current_date) - {age}"
            condition_query += f"\nAND v.visit_concept_id = {visit_concept_id}"
            if resolved.get("year"):
                condition_query += f"\nAND EXTRACT(YEAR FROM v.visit_start_date) = {resolved['year']}"
            condition_query += "\nGROUP BY p.person_id, p.year_of_birth"
    
    return condition_query
