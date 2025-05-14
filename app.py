import streamlit as st
from agents.input_parser_agent import parse_question
from agents.concept_resolver_agent import resolve
from agents.sql_generator_agent import generate
from agents.query_executor_agent import execute
from agents.summarizer_agent import summarize

st.title("OMOP Agent Pipeline")

# Add example queries section
st.markdown("""
### Example Queries
You can use natural language to query the database. Here are some examples:

**Simple Conditions:**
- "Find patients with diabetes"
- "Find patients with hypertension"
- "Find patients with diabetes and hypertension"

**Visit Types:**
- "Find patients with ER visits"
- "Find patients with hospitalizations"
- "Find patients with ER visits since 2020"
- "Find patients with hospitalizations since 2020"

**Combined Queries:**
- "Find patients with diabetes who had ER visits"
- "Find patients with hypertension who had hospitalizations"
- "Find patients over age 65 with diabetes"
- "Find patients with diabetes who had hospitalizations since 2020"
""")

# Add five main buttons in five columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button('Diabetes & Hypertension'):
        user_question = 'Find patients with diabetes and hypertension'
        st.session_state['user_question'] = user_question
        parsed_output = parse_question(user_question)
        resolved = resolve(parsed_output)
        sql = generate(resolved)
        results = execute(sql)
        summary = summarize(results)
        
        with st.expander("View Intermediate Outputs"):
            st.write("Parsed Output:", parsed_output)
            st.write("Resolved Concepts:", resolved)
            st.write("Generated SQL:", sql)
            st.write("Query Results Shape:", results.shape)
            st.write("First few rows of results:", results.head())
        
        st.write("### Patients with Both Diabetes and Hypertension")
        st.write(summary)

with col2:
    if st.button('ER Visits'):
        user_question = "Find patients with ER visits"
        st.session_state['user_question'] = user_question
        parsed_output = parse_question(user_question)
        resolved = resolve(parsed_output)
        sql = generate(resolved)
        results = execute(sql)
        summary = summarize(results)
        
        with st.expander("View Intermediate Outputs"):
            st.write("Parsed Output:", parsed_output)
            st.write("Resolved Concepts:", resolved)
            st.write("Generated SQL:", sql)
            st.write("Query Results Shape:", results.shape)
            st.write("First few rows of results:", results.head())
        
        st.write("### Emergency Room Visits")
        st.write(summary)

with col3:
    if st.button('Hospitalizations'):
        user_question = "Find patients with hospitalizations"
        st.session_state['user_question'] = user_question
        parsed_output = parse_question(user_question)
        resolved = resolve(parsed_output)
        sql = generate(resolved)
        results = execute(sql)
        summary = summarize(results)
        
        with st.expander("View Intermediate Outputs"):
            st.write("Debug - Parsed Output:", parsed_output)
            st.write("Debug - Resolved Concepts:", resolved)
            st.write("Debug - Generated SQL:", sql)
            st.write("Debug - Results Shape:", results.shape)
            st.write("Debug - Results Columns:", results.columns)
            st.write("Debug - First few rows:", results.head())
        
        st.write("### Hospital Inpatient Visits")
        st.write(summary)

with col4:
    if st.button('Diabetes Only'):
        user_question = "Find patients with diabetes"
        st.session_state['user_question'] = user_question
        parsed_output = parse_question(user_question)
        resolved = resolve(parsed_output)
        sql = generate(resolved)
        results = execute(sql)
        summary = summarize(results)
        
        with st.expander("View Intermediate Outputs"):
            st.write("Parsed Output:", parsed_output)
            st.write("Resolved Concepts:", resolved)
            st.write("Generated SQL:", sql)
            st.write("Query Results Shape:", results.shape)
            st.write("First few rows of results:", results.head())
        
        st.write("### Patients with Diabetes")
        st.write(summary)

with col5:
    if st.button('Hypertension Only'):
        user_question = "Find patients with hypertension"
        st.session_state['user_question'] = user_question
        parsed_output = parse_question(user_question)
        resolved = resolve(parsed_output)
        sql = generate(resolved)
        results = execute(sql)
        summary = summarize(results)
        
        with st.expander("View Intermediate Outputs"):
            st.write("Parsed Output:", parsed_output)
            st.write("Resolved Concepts:", resolved)
            st.write("Generated SQL:", sql)
            st.write("Query Results Shape:", results.shape)
            st.write("First few rows of results:", results.head())
        
        st.write("### Patients with Hypertension")
        st.write(summary)

# Add custom query input
st.markdown("---")
st.markdown("### Custom Query")
user_question = st.text_input("Or enter your own query:", "Find patients with diabetes")

if st.button("Run Custom Query"):
    st.write("=== Testing OMOP Agent Pipeline ===")
    st.write(f"Input Question: {user_question}")

    # 1. Input Parser Agent
    parsed_output = parse_question(user_question)
    # 2. Concept Resolver Agent
    resolved_concepts = resolve(parsed_output)
    # 3. SQL Generator Agent
    sql_query = generate(resolved_concepts)
    # 4. Query Executor Agent
    query_results = execute(sql_query)
    # 5. Summarizer Agent
    summary = summarize(query_results)

    # Display intermediate outputs in an expander
    with st.expander("View Intermediate Outputs"):
        st.write("1. Input Parser Agent:")
        st.write("Parsed Output:", parsed_output)
        st.write("2. Concept Resolver Agent:")
        st.write("Resolved Concepts:", resolved_concepts)
        st.write("3. SQL Generator Agent:")
        st.write("Generated SQL:")
        st.code(sql_query, language="sql")

    # Display query results and final summary prominently
    st.write("### Results")
    st.write(summary) 