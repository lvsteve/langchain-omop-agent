import streamlit as st
from agents import input_parser_agent, concept_resolver_agent, sql_generator_agent, query_executor_agent, summarizer_agent

st.title("OMOP Natural Language Query Agent")

user_input = st.text_input("Enter your question", "Find patients over age 65 with diabetes and hypertension")

if st.button("Run Analysis"):
    with st.spinner("Parsing and querying..."):
        parsed = input_parser_agent.parse_question(user_input)
        resolved = concept_resolver_agent.resolve(parsed)
        query = sql_generator_agent.generate(resolved)
        result_df = query_executor_agent.execute(query)
        summary = summarizer_agent.summarize(result_df)

    st.subheader("Summary")
    st.write(summary)

    st.subheader("Sample Results")
    st.dataframe(result_df.head(20))
