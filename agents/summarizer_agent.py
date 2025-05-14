import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime

def summarize(df):
    """
    Generate a comprehensive summary of the data in a human-readable format.
    
    Args:
        df (pandas.DataFrame): Input DataFrame with columns:
            - year: Year of the data
            - visit_type: Type of visit (Inpatient, ER, etc.)
            - patients: Number of unique patients
            - total_visits: Total number of visits
    
    Returns:
        str: Formatted summary of the data with tables and visual separators
    """
    if df.empty:
        return "No data available to summarize."
    
    # Fallback: If DataFrame does not have expected columns, just count rows
    if not all(col in df.columns for col in ['patients', 'total_visits']):
        count = len(df)
        return f"Found {count} patients meeting the criteria."
    
    # Basic statistics
    total_patients = df['patients'].sum()
    total_visits = df['total_visits'].sum()
    avg_visits_per_patient = total_visits / total_patients
    
    # Calculate year-over-year changes
    df['year'] = df['year'].astype(int)
    years = sorted(df['year'].unique())
    
    # Visit type breakdown
    visit_type_stats = df.groupby('visit_type').agg({
        'patients': 'sum',
        'total_visits': 'sum'
    }).round(2)
    visit_type_stats['avg_visits_per_patient'] = visit_type_stats['total_visits'] / visit_type_stats['patients']
    
    # Calculate trends
    yearly_totals = df.groupby('year').agg({
        'patients': 'sum',
        'total_visits': 'sum'
    })
    
    # Calculate year-over-year changes
    yoy_changes = yearly_totals.pct_change() * 100
    
    # Build the summary
    summary = []
    
    # Header
    summary.append("=" * 80)
    summary.append("HEALTHCARE UTILIZATION SUMMARY REPORT")
    summary.append("=" * 80)
    summary.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("-" * 80)
    
    # Overall Statistics Table
    summary.append("\nOVERALL STATISTICS")
    summary.append("-" * 40)
    overall_stats = [
        ["Total Unique Patients", f"{total_patients:,}"],
        ["Total Visits", f"{total_visits:,}"],
        ["Average Visits per Patient", f"{avg_visits_per_patient:.2f}"]
    ]
    summary.append(tabulate(overall_stats, tablefmt="grid"))
    
    # Visit Type Breakdown Table
    summary.append("\nVISIT TYPE BREAKDOWN")
    summary.append("-" * 40)
    visit_type_table = visit_type_stats.reset_index()
    visit_type_table.columns = ['Visit Type', 'Total Patients', 'Total Visits', 'Avg Visits/Patient']
    visit_type_table = visit_type_table.round(2)
    summary.append(tabulate(visit_type_table, headers='keys', tablefmt="grid", showindex=False))
    
    # Year-over-Year Trends Table
    summary.append("\nYEAR-OVER-YEAR TRENDS")
    summary.append("-" * 40)
    trend_data = []
    for year in years[1:]:
        prev_year = year - 1
        if prev_year in yoy_changes.index:
            patient_change = yoy_changes.loc[year, 'patients']
            visit_change = yoy_changes.loc[year, 'total_visits']
            trend_data.append([
                f"{prev_year} → {year}",
                f"{patient_change:+.1f}%",
                f"{visit_change:+.1f}%"
            ])
    summary.append(tabulate(trend_data, 
                          headers=['Period', 'Patient Change', 'Visit Change'],
                          tablefmt="grid"))
    
    # Key Insights
    summary.append("\nKEY INSIGHTS")
    summary.append("-" * 40)
    
    # Most recent year stats
    latest_year = max(years)
    latest_data = df[df['year'] == latest_year]
    if not latest_data.empty:
        summary.append(f"\nMost Recent Year ({latest_year}) Statistics:")
        latest_stats = []
        for _, row in latest_data.iterrows():
            latest_stats.append([
                row['visit_type'],
                f"{row['patients']:,}",
                f"{row['total_visits']:,}"
            ])
        summary.append(tabulate(latest_stats,
                              headers=['Visit Type', 'Patients', 'Total Visits'],
                              tablefmt="grid"))
    
    # Overall trend
    if len(years) > 1:
        first_year_patients = yearly_totals.loc[min(years), 'patients']
        last_year_patients = yearly_totals.loc[max(years), 'patients']
        overall_patient_change = ((last_year_patients - first_year_patients) / first_year_patients) * 100
        
        first_year_visits = yearly_totals.loc[min(years), 'total_visits']
        last_year_visits = yearly_totals.loc[max(years), 'total_visits']
        overall_visit_change = ((last_year_visits - first_year_visits) / first_year_visits) * 100
        
        summary.append(f"\nOverall Trend ({min(years)} to {max(years)}):")
        trend_stats = [
            ["Patient Change", f"{overall_patient_change:+.1f}%"],
            ["Visit Change", f"{overall_visit_change:+.1f}%"]
        ]
        summary.append(tabulate(trend_stats, tablefmt="grid"))
    
    # Footer
    summary.append("\n" + "=" * 80)
    
    return "\n".join(summary)
