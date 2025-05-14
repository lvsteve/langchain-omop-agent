def generate(resolved):
    concept_ids = ', '.join(map(str, resolved["concept_ids"]))
    return f"""SELECT person_id, year_of_birth FROM person
    WHERE year_of_birth <= extract(year from current_date) - 65
    AND person_id IN (
        SELECT person_id FROM condition_occurrence
        WHERE condition_concept_id IN ({concept_ids})
    )"""
