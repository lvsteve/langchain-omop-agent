import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URI"))

# Query: Patients and member months by year from 2016 to present
enrollment_query = '''
WITH years AS (
    SELECT generate_series(2016, EXTRACT(YEAR FROM CURRENT_DATE))::int AS year
),
periods AS (
    SELECT person_id, observation_period_start_date, observation_period_end_date FROM cdm.observation_period
),
expanded AS (
    SELECT
        y.year,
        p.person_id,
        GREATEST(p.observation_period_start_date, make_date(y.year, 1, 1)) AS start_date,
        LEAST(p.observation_period_end_date, make_date(y.year, 12, 31)) AS end_date
    FROM years y
    JOIN periods p
      ON p.observation_period_start_date <= make_date(y.year, 12, 31)
     AND p.observation_period_end_date >= make_date(y.year, 1, 1)
)
SELECT
    year,
    COUNT(DISTINCT person_id) AS member_count,
    SUM(EXTRACT(MONTH FROM age(end_date + INTERVAL '1 day', start_date))) +
    SUM((EXTRACT(YEAR FROM age(end_date + INTERVAL '1 day', start_date))) * 12) AS member_months
FROM expanded
GROUP BY year
ORDER BY year;
'''

with engine.connect() as conn:
    print("\nPatients and Member Months by Year (2016-present):")
    print("Year\tPatients\tMember Months")
    print("-" * 40)
    result = conn.execute(text(enrollment_query))
    for row in result:
        print(f"{int(row[0])}\t{row[1]}\t{int(row[2])}") 