import streamlit as st
import pandas as pd
from rate_calculator import calculate_event_table

# Set page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Event Rate Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Event Rate Dashboard")

def format_table(df):
    # Format the rate column to always show one decimal place
    df['Rate per 1000 Member Months'] = df['Rate per 1000 Member Months'].map('{:.1f}'.format)
    
    # Define column configuration for centered content
    column_config = {
        'Year': st.column_config.NumberColumn(
            'Year',
            width='medium',
            help='Year of data',
            format='%d'
        ),
        'Total Members': st.column_config.NumberColumn(
            'Total Members',
            width='medium',
            help='Total number of members enrolled',
            format='%d'
        ),
        'Members with ER Event': st.column_config.NumberColumn(
            'Members with ER Event',
            width='medium',
            help='Number of members with at least one event',
            format='%d'
        ),
        'Total ER Events': st.column_config.NumberColumn(
            'Total ER Events',
            width='medium',
            help='Total number of events',
            format='%d'
        ),
        'Member Months': st.column_config.NumberColumn(
            'Member Months',
            width='medium',
            help='Total member months',
            format='%d'
        ),
        'Rate per 1000 Member Months': st.column_config.NumberColumn(
            'Rate per 1000 Member Months',
            width='medium',
            help='Rate per 1000 member months',
            format='%.1f'
        )
    }
    
    # Apply custom CSS to center headers and content
    st.markdown("""
        <style>
            div[data-testid="stDataFrame"] table {
                text-align: center !important;
            }
            div[data-testid="stDataFrame"] th {
                text-align: center !important;
            }
            div[data-testid="stDataFrame"] td {
                text-align: center !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    return df, column_config

# Create two columns for the buttons
col1, col2 = st.columns(2)

# Add buttons in the columns
with col1:
    er_button = st.button("Show ER Visit Rates", type="primary")
with col2:
    hosp_button = st.button("Show Hospitalization Rates", type="primary")

# Initialize session state for tracking which table to show
if 'show_table' not in st.session_state:
    st.session_state.show_table = None

# Update session state based on button clicks
if er_button:
    st.session_state.show_table = 'er'
if hosp_button:
    st.session_state.show_table = 'hospital'

# Display the selected table
if st.session_state.show_table == 'er':
    st.header("ER Visit Rates")
    er_df = calculate_event_table('er')
    er_df.rename(columns={
        'year': 'Year',
        'total_members': 'Total Members',
        'members_with_event': 'Members with ER Event',
        'total_events': 'Total ER Events',
        'member_months': 'Member Months',
        'rate_per_1000': 'Rate per 1000 Member Months'
    }, inplace=True)
    df, config = format_table(er_df)
    st.dataframe(df, column_config=config, hide_index=True)

elif st.session_state.show_table == 'hospital':
    st.header("Hospitalization Rates")
    hosp_df = calculate_event_table('hospital')
    hosp_df.rename(columns={
        'year': 'Year',
        'total_members': 'Total Members',
        'members_with_event': 'Members with Hospital Event',
        'total_events': 'Total Hospital Events',
        'member_months': 'Member Months',
        'rate_per_1000': 'Rate per 1000 Member Months'
    }, inplace=True)
    df, config = format_table(hosp_df)
    st.dataframe(df, column_config=config, hide_index=True)

else:
    st.info("👆 Select a table to display using the buttons above") 