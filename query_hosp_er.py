import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URI"))

query = '''
WITH years AS (
    SELECT generate_series(2016, EXTRACT(YEAR FROM CURRENT_DATE))::int AS year
),
visits AS (
    SELECT person_id, visit_start_date, visit_concept_id
    FROM cdm.visit_occurrence
    WHERE visit_concept_id IN (9201, 9203, 262)
),
expanded AS (
    SELECT
        y.year,
        v.person_id,
        v.visit_start_date,
        v.visit_concept_id
    FROM years y
    JOIN visits v
      ON EXTRACT(YEAR FROM v.visit_start_date) = y.year
),
member_stats AS (
    SELECT
        y.year,
        COUNT(DISTINCT p.person_id) AS total_members,
        COUNT(*) AS member_months
    FROM years y
    CROSS JOIN LATERAL (
        SELECT person_id
        FROM cdm.observation_period
        WHERE EXTRACT(YEAR FROM observation_period_start_date) <= y.year
        AND EXTRACT(YEAR FROM observation_period_end_date) >= y.year
    ) p
    GROUP BY y.year
)
SELECT
    e.year,
    CASE e.visit_concept_id
        WHEN 9201 THEN 'Inpatient'
        WHEN 9203 THEN 'ER'
        WHEN 262 THEN 'ER+Inpatient'
    END AS visit_type,
    ms.total_members,
    ms.member_months,
    COUNT(DISTINCT e.person_id) AS patients_with_visits,
    COUNT(*) AS total_visits,
    ROUND((COUNT(*) * 1000.0 / ms.member_months), 2) AS visits_per_1000_member_months
FROM expanded e
JOIN member_stats ms ON e.year = ms.year
GROUP BY e.year, e.visit_concept_id, ms.total_members, ms.member_months
ORDER BY e.year, e.visit_concept_id;
'''

with engine.connect() as conn:
    print("\nHospitalization and ER Visits by Type and Year (2016-present):")
    print("Year\tVisit Type\tTotal Members\tMember Months\tPatients with Visits\tTotal Visits\tVisits per 1000 Member Months")
    print("-" * 100)
    result = conn.execute(text(query))
    for row in result:
        print(f"{int(row[0])}\t{row[1]}\t{row[2]}\t{int(row[3])}\t{row[4]}\t{row[5]}\t{row[6]}") 