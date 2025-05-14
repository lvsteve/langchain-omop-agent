# OMOP Agent Pipeline

A natural language interface for querying OMOP CDM databases, built using LangChain and Streamlit.

## Current Architecture

The agent chain consists of five main components:

1. **Input Parser Agent**
   - Parses natural language questions into structured data
   - Extracts conditions, visit types, age filters, and years
   - Uses regex patterns for reliable extraction

2. **Concept Resolver Agent**
   - Maps conditions and visit types to OMOP concept IDs
   - Handles special cases like hypertension (multiple concept IDs)
   - Supports diabetes, hypertension, ER visits, and hospitalizations

3. **SQL Generator Agent**
   - Generates SQL queries based on resolved concepts
   - Supports various query types:
     - Single conditions (e.g., diabetes only)
     - Multiple conditions (e.g., diabetes and hypertension)
     - Visit types (ER visits, hospitalizations)
     - Combined queries (conditions with visit types)

4. **Query Executor Agent**
   - Executes SQL queries using SQLAlchemy and Pandas
   - Handles database connections securely
   - Returns results as Pandas DataFrames

5. **Summarizer Agent**
   - Formats query results into readable tables
   - Provides yearly breakdowns
   - Calculates totals and percentages

## Current Technologies

- **Database Access**: Direct SQL queries to OMOP CDM tables using SQLAlchemy
- **Data Processing**: Pandas for query execution and data manipulation
- **Web Interface**: Streamlit for interactive querying
- **Natural Language Processing**: Custom regex-based parsing
- **Agent Framework**: LangChain for agent orchestration

## Future Enhancements

### 1. OMOP Integration
- Integrate [pyomop](https://github.com/OHDSI/pyomop) for:
  - Standardized OMOP concept handling
  - Built-in OMOP query templates
  - Better concept hierarchy support
  - Improved vocabulary management

### 2. Advanced Agent Framework
- Migrate to [CrewAI](https://github.com/joaomdmoura/crewAI) for:
  - More sophisticated agent collaboration
  - Better task decomposition
  - Improved error handling
  - Enhanced agent communication

### 3. Statistical Analysis Agent
- Add statistical capabilities:
  - Trend analysis over time
  - Patient demographics analysis
  - Comorbidity analysis
  - Risk factor identification
  - Statistical significance testing

### 4. Report Generation Agent
- Implement automated report generation:
  - PDF report creation
  - Data visualization
  - Executive summaries
  - Key findings extraction
  - Customizable report templates

### 5. Enhanced Natural Language Understanding
- Improve question parsing:
  - Support for more complex queries
  - Better handling of temporal relationships
  - Improved condition combinations
  - Support for medication queries
  - Procedure-based queries

### 6. Data Quality and Validation
- Add data quality checks:
  - Data completeness validation
  - Consistency checks
  - Outlier detection
  - Data quality metrics
  - Automated data cleaning

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with database credentials
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Testing

Run individual test scripts:
```bash
python test_diabetes.py
python test_hypertension.py
python test_diabetes_hypertension.py
python test_er_visits.py
python test_hospitalizations.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
