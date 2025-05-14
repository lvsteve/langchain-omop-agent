from agents import input_parser_agent, concept_resolver_agent, sql_generator_agent, query_executor_agent, summarizer_agent

def run_omop_pipeline(question: str):
    parsed = input_parser_agent.parse_question(question)
    resolved = concept_resolver_agent.resolve(parsed)
    query = sql_generator_agent.generate(resolved)
    result_df = query_executor_agent.execute(query)
    summary = summarizer_agent.summarize(result_df)
    print(summary)

if __name__ == "__main__":
    run_omop_pipeline("Find patients over age 65 with diabetes and hypertension")
