import pandas as pd
from sqlalchemy import text
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.db_connection import get_connection

def calculate_event_table(visit_type='er'):
    """
    Calculate yearly event table for ER or hospitalizations.
    Args:
        visit_type: 'er' for ER visits (concept_id 9203) or 'hospital' for hospitalizations (concept_id 9201)
    Returns a DataFrame with columns:
        year, total_members, members_with_event, total_events, member_months, rate_per_1000
    """
    concept_id = 9203 if visit_type == 'er' else 9201
    query = """
    WITH member_months AS (
        SELECT 
            EXTRACT(YEAR FROM visit_start_date) AS year,
            person_id,
            COUNT(DISTINCT DATE_TRUNC('month', visit_start_date)) AS months_present
        FROM cdm.visit_occurrence
        WHERE visit_start_date >= '2016-01-01'
        GROUP BY EXTRACT(YEAR FROM visit_start_date), person_id
    ),
    yearly_member_months AS (
        SELECT 
            year,
            COUNT(DISTINCT person_id) AS total_members,
            SUM(months_present) AS member_months
        FROM member_months
        GROUP BY year
    ),
    yearly_events AS (
        SELECT 
            EXTRACT(YEAR FROM visit_start_date) AS year,
            COUNT(*) AS total_events,
            COUNT(DISTINCT person_id) AS members_with_event
        FROM cdm.visit_occurrence
        WHERE visit_concept_id = :concept_id
        AND visit_start_date >= '2016-01-01'
        GROUP BY EXTRACT(YEAR FROM visit_start_date)
    )
    SELECT 
        CAST(m.year AS INTEGER) AS year,
        m.total_members,
        COALESCE(e.members_with_event, 0) AS members_with_event,
        COALESCE(e.total_events, 0) AS total_events,
        CAST(m.member_months AS INTEGER) AS member_months,
        ROUND(COALESCE(e.total_events, 0) * 1000.0 / NULLIF(m.member_months, 0), 2) AS rate_per_1000
    FROM yearly_member_months m
    LEFT JOIN yearly_events e ON m.year = e.year
    ORDER BY year;
    """
    with get_connection() as conn:
        df = pd.read_sql(text(query), conn, params={'concept_id': concept_id})
    return df

def format_event_table(df, visit_type):
    """
    Format the event table results into a readable table.
    """
    visit_type_display = "ER" if visit_type == 'er' else "Hospital"
    headers = [
        'Year',
        'Total Members',
        f'Members with {visit_type_display} Event',
        f'Total {visit_type_display} Events',
        'Member Months',
        f'Rate per 1000 Member Months'
    ]
    table = df.to_string(index=False, header=headers, float_format=lambda x: '{:.2f}'.format(x) if isinstance(x, float) else str(int(x)) if isinstance(x, (int, float)) and x == int(x) else str(x))
    return f"\n{'-' * 100}\n{table}\n{'-' * 100}"

if __name__ == "__main__":
    print("\nER Event Table:")
    er_df = calculate_event_table('er')
    print(format_event_table(er_df, 'er'))
    print("\nHospitalization Event Table:")
    hosp_df = calculate_event_table('hospital')
    print(format_event_table(hosp_df, 'hospital')) 