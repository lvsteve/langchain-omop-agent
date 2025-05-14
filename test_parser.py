from agents.input_parser_agent import parse_question

questions = [
    "Find patients over age 65 with diabetes and hypertension",
    "Show me patients with type 1 diabetes",
    "What is the total number of inpatient visits for patients with essential hypertension?",
    "How many ER visits for patients with asthma in 2023?",
    "List patients with COPD",
    "Find patients with diabetes or hypertension",
    "Show me patients over age 50 with asthma and COPD in 2020",
    "Find patients with type 2 diabetes who visited the hospital in 2021"
]

for i, q in enumerate(questions, 1):
    print(f"\n=== Test {i} ===")
    print(f"Question: {q}")
    parsed = parse_question(q)
    print(f"Parsed: {parsed}") 