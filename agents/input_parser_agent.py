import re

def parse_question(question: str):
    """
    Parse a simple natural language question into structured data.

    Supported question types (keep it simple!):
      - Find patients over age 65 with diabetes and hypertension
      - Show me patients with type 1 diabetes
      - What is the total number of inpatient visits for patients with essential hypertension?
      - How many ER visits for patients with asthma in 2023?

    Supported features:
      - Age filter: 'over age N'
      - Condition(s): after 'with', 'having', or 'diagnosed with', split on 'and'/'or'
      - Visit type: 'ER', 'inpatient', 'hospital', 'hospitalizations'
      - Year: 'in 2023', etc.

    Avoid complex or multi-part questions for now.
    """
    question = question.lower()
    # Remove punctuation except numbers (for years/ages)
    question = re.sub(r'[^a-z0-9\s]', '', question)

    result = {
        "conditions": [],
        "age_filter": None,
        "visit_type": None,
        "year": None
    }

    # Extract age filter
    match = re.search(r'over age (\d+)', question)
    if match:
        result["age_filter"] = f"age > {match.group(1)}"

    # Extract year
    match = re.search(r'in (\d{4})', question)
    if match:
        result["year"] = int(match.group(1))

    # Extract visit type using whole word matching
    if re.search(r'\ber\b', question):
        result["visit_type"] = "ER"
    elif re.search(r'\binpatient\b', question) or re.search(r'\bhospital\b', question) or re.search(r'\bhospitalizations\b', question):
        result["visit_type"] = "Inpatient"

    # Extract conditions
    cond = None
    for kw in ["with", "having", "diagnosed with"]:
        if kw in question:
            cond = question.split(kw, 1)[1]
            break
    if cond:
        # Split on 'and' or 'or'
        conds = re.split(r'\band\b|\bor\b', cond)
        conds = [c.strip() for c in conds if c.strip()]
        result["conditions"] = conds
    return result
