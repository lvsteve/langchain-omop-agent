import os
from dotenv import load_dotenv
from agents import (
    input_parser_agent,
    concept_resolver_agent,
    sql_generator_agent,
    query_executor_agent,
    summarizer_agent
)

def test_pipeline(question: str):
    print("\n=== Testing OMOP Agent Pipeline ===")
    print(f"Input Question: {question}")
    print("\n1. Input Parser Agent:")
    parsed = input_parser_agent.parse_question(question)
    print(f"Parsed Output: {parsed}")
    
    print("\n2. Concept Resolver Agent:")
    resolved = concept_resolver_agent.resolve(parsed)
    print(f"Resolved Concepts: {resolved}")
    
    print("\n3. SQL Generator Agent:")
    query = sql_generator_agent.generate(resolved)
    print(f"Generated SQL:\n{query}")
    
    print("\n4. Query Executor Agent:")
    try:
        result_df = query_executor_agent.execute(query)
        print(f"Query Results Shape: {result_df.shape}")
        print("\nFirst few rows:")
        print(result_df.head())
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return
    
    print("\n5. Summarizer Agent:")
    try:
        summary = summarizer_agent.summarize(result_df)
        print("\nFinal Summary:")
        print(summary)
    except Exception as e:
        print(f"Error generating summary: {str(e)}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Test cases
    test_cases = [
        "Find patients over age 65 with diabetes and hypertension",
        "Show me patients with type 1 diabetes who visited the ER in 2023",
        "What is the total number of inpatient visits for patients with essential hypertension?",
        "Find patients with hospitalizations since 2020"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n\n=== Test Case {i} ===")
        test_pipeline(question)
        print("\n" + "="*50) 