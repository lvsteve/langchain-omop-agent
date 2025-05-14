from agents import (
    input_parser_agent,
    concept_resolver_agent,
    sql_generator_agent,
    query_executor_agent,
    summarizer_agent
)

def test_input_parser():
    question = "Find patients over age 65 with diabetes and hypertension"
    result = input_parser_agent.parse_question(question)
    print("\n=== Input Parser Test ===")
    print(f"Input: {question}")
    print(f"Output: {result}")

def test_concept_resolver():
    parsed_input = input_parser_agent.parse_question("Find patients over age 65 with diabetes and hypertension")
    result = concept_resolver_agent.resolve(parsed_input)
    print("\n=== Concept Resolver Test ===")
    print(f"Input: {parsed_input}")
    print(f"Output: {result}")

def test_sql_generator():
    parsed = input_parser_agent.parse_question("Find patients over age 65 with diabetes and hypertension")
    resolved = concept_resolver_agent.resolve(parsed)
    result = sql_generator_agent.generate(resolved)
    print("\n=== SQL Generator Test ===")
    print(f"Input: {resolved}")
    print(f"Output: {result}")

def test_query_executor():
    query = "SELECT * FROM cdm.person WHERE year_of_birth <= extract(year from current_date) - 65"
    result = query_executor_agent.execute(query)
    print("\n=== Query Executor Test ===")
    print(f"Input: {query}")
    print(f"Output: {result}")

def test_summarizer():
    # Create a sample DataFrame or use actual query results
    import pandas as pd
    sample_data = pd.DataFrame({
        'patient_id': [1, 2, 3],
        'age': [70, 75, 68],
        'condition': ['diabetes', 'hypertension', 'both']
    })
    result = summarizer_agent.summarize(sample_data)
    print("\n=== Summarizer Test ===")
    print("Input: Sample DataFrame")
    print(f"Output: {result}")

if __name__ == "__main__":
    # Test each agent individually
    test_input_parser()
    test_concept_resolver()
    test_sql_generator()
    test_query_executor()
    test_summarizer() 