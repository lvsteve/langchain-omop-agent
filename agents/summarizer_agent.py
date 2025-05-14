import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime

def summarize(results):
    """
    Generate a comprehensive summary of the data in a human-readable format.
    
    Args:
        results (pandas.DataFrame): Input DataFrame with columns:
            - visit_year: Year of the data
            - patient_count: Number of unique patients
            - visit_count or record_count: Count of visits or records
    
    Returns:
        str: Formatted summary of the data with tables and visual separators
    """
    if results.empty:
        return "No data available to summarize."
    
    # Create a copy to avoid the SettingWithCopyWarning
    results = results.copy()
    
    # Filter to 2016 and later, and remove future years
    current_year = pd.Timestamp.now().year
    results = results[
        (results['visit_year'] >= 2016) & 
        (results['visit_year'] <= current_year)
    ]
    
    # Convert year to integer for proper sorting
    results.loc[:, 'visit_year'] = results['visit_year'].astype(int)
    results = results.sort_values('visit_year')
    
    # Determine the appropriate column name based on the data
    if 'visit_count' in results.columns:
        count_column = 'visit_count'
        last_column = 'Total Visits'
    else:
        count_column = 'record_count'
        last_column = 'Total Records'
    
    # Format the results into a table
    table_data = []
    for _, row in results.iterrows():
        table_data.append([
            int(row['visit_year']),
            f"{int(row['patient_count']):,}",
            f"{int(row[count_column]):,}"
        ])
    
    # Add total row
    total_patients = results['patient_count'].sum()
    total_count = results[count_column].sum()
    table_data.append([
        '**Total**',
        f"**{int(total_patients):,}**",
        f"**{int(total_count):,}**"
    ])
    
    headers = ['Year', 'Unique Patients', last_column]
    
    # Create the table with wider columns and better formatting
    table = tabulate(
        table_data,
        headers=headers,
        tablefmt='pipe',
        numalign='right',
        colalign=('right', 'right', 'right'),
        stralign='right',
        disable_numparse=True  # This prevents number parsing which can cause alignment issues
    )
    
    # Add a line of dashes above and below the table
    separator = '-' * 80  # Make the separator wider
    formatted_table = f"\n{separator}\n{table}\n{separator}"
    
    return formatted_table
