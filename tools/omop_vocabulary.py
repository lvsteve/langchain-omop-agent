from tools.db_connection import get_connection

def lookup_concepts(term):
    sql = f"""SELECT concept_id FROM concept
             WHERE lower(concept_name) = lower('{term}')
             AND domain_id = 'Condition'
             LIMIT 5"""
    with get_connection() as conn:
        result = conn.execute(sql)
        return [row[0] for row in result]
