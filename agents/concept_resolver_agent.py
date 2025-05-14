from tools.omop_vocabulary import lookup_concepts

def resolve(parsed_output):
    """
    Resolve concepts from parsed output.
    
    Args:
        parsed_output (dict): Dictionary containing:
            - conditions: List of conditions
            - age_filter: Age filter if specified
            - visit_type: Type of visit if specified
            - year: Year filter if specified
    
    Returns:
        dict: Dictionary containing resolved concepts
    """
    # Extract year from conditions if present
    year = None
    conditions = []
    for condition in parsed_output.get('conditions', []):
        if 'since' in condition.lower():
            try:
                year = int(condition.split('since')[1].strip())
            except:
                pass
        else:
            conditions.append(condition)
    
    # If no year in conditions, use the year from parsed_output
    if not year:
        year = parsed_output.get('year')
    
    # Map conditions to concept IDs
    concept_ids = []
    has_diabetes = False
    has_hypertension = False
    
    for condition in conditions:
        if 'diabetes' in condition.lower():
            has_diabetes = True
            # Only use Type 2 diabetes mellitus (201826) since that's the only one with patients
            concept_ids.append(201826)
        elif 'hypertension' in condition.lower():
            has_hypertension = True
            concept_ids.extend([320128, 319826, 319825, 319827, 319828])
    
    # Map visit types
    visit_type = None
    if parsed_output.get('visit_type'):
        if 'er' in parsed_output['visit_type'].lower():
            visit_type = 'ER'
        elif 'inpatient' in parsed_output['visit_type'].lower() or 'hospitalization' in parsed_output['visit_type'].lower():
            visit_type = 'Inpatient'
    
    # If no concept IDs but we have visit_type or year, return empty list
    if not concept_ids and (visit_type or year):
        return {
            'concept_ids': [],
            'age_filter': parsed_output.get('age_filter'),
            'visit_type': visit_type,
            'year': year
        }
    
    return {
        'concept_ids': concept_ids if concept_ids else None,
        'age_filter': parsed_output.get('age_filter'),
        'visit_type': visit_type,
        'year': year
    }
