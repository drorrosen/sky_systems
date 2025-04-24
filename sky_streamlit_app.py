import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import calendar
from PIL import Image
from io import BytesIO
import base64
import urllib.request
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components
import random
import yaml



# Set page configuration
st.set_page_config(
    page_title="Sky Systemz Dashboard",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    :root {
        --sky-primary: #1E88E5;
        --sky-secondary: #2196F3;
        --sky-accent: #0D47A1;
        --sky-dark: #1f2937;
        --sky-light: #f5f7fa;
        --sky-gray: #6b7280;
    }
    
    .main {
        background-color: #f5f7fa;
    }
    
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: var(--sky-dark);
        margin-bottom: 5px;
    }
    
    .metric-label {
        font-size: 14px;
        color: var(--sky-gray);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
    }
    
    .data-table {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .stSelectbox label, .stDateInput label {
        color: var(--sky-dark);
        font-weight: 600;
    }
    
    .stDataFrame {
        border-radius: 10px;
    }
    
    .not-eligible {
        color: #ef4444;
        font-weight: bold;
    }
    
    .eligible {
        color: #10b981;
        font-weight: bold;
    }
    
    .completion-high {
        color: #10b981;
        font-weight: bold;
    }
    
    .completion-medium {
        color: #f59e0b;
        font-weight: bold;
    }
    
    .completion-low {
        color: #ef4444;
        font-weight: bold;
    }
    
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .logo-img {
        max-height: 60px;
    }
    
    /* Login page styling */
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 40px;
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        margin-top: 80px;
        border: 1px solid rgba(33, 150, 243, 0.1);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 30px;
        color: var(--sky-dark);
        font-weight: 700;
    }
    
    .login-subheader {
        text-align: center;
        margin-bottom: 30px;
        color: var(--sky-gray);
        font-size: 16px;
    }
    
    .login-button {
        background-color: var(--sky-primary);
        color: white;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        width: 100%;
        border: none;
        cursor: pointer;
        transition: all 0.2s;
        margin-top: 20px;
    }
    
    .login-button:hover {
        background-color: var(--sky-secondary);
        transform: translateY(-2px);
    }
    
    .centered-logo {
        display: block;
        margin: 0 auto;
        margin-bottom: 60px;
        width: 360px;
    }
    
    .user-type-selector {
        margin-bottom: 30px;
        background-color: #f9fafb;
        padding: 15px;
        border-radius: 10px;
    }
    
    /* Gradient text for headings */
    .gradient-text {
        background: linear-gradient(90deg, var(--sky-primary), var(--sky-accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Custom sidebar styling */
    .sidebar .sidebar-content {
        background-color: white;
    }
    
    /* Custom button styling */
    .stButton>button {
        background-color: var(--sky-primary);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px 20px;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: var(--sky-secondary);
        transform: translateY(-2px);
    }
    
    /* Custom radio button styling */
    .stRadio>div {
        padding: 10px;
        display: flex;
        gap: 20px;
    }
    
    /* Custom text input styling */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        padding: 12px 16px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--sky-primary);
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
    }
    
    /* Remove white backgrounds from all containers */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: transparent;
        border: none;
        padding: 0;
        box-shadow: none;
    }
    
    /* Remove white backgrounds from metric cards */
    div.css-1xarl3l.e16fv1kl0 {
        background-color: transparent;
        border: none;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Style for metric cards */
    .metric-card {
        background-color: transparent;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Style for charts */
    .chart-container {
        background-color: transparent;
        padding: 0;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Remove borders from all elements */
    .element-container, .stDataFrame, .stPlotlyChart {
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Remove padding from main container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Style for section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #1f2937;
    }
    
    /* Remove ALL white borders and containers */
    .main > .block-container {
        padding-top: 0 !important;
        padding-right: 0 !important;
        padding-left: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Fix background color consistency */
    .stApp {
        background-color: #f5f7fa;
    }
    
    /* Remove default Streamlit element margins/padding */
    .element-container, .stButton, .stRadio, .stSelectbox, .stDateInput {
        margin-bottom: 0.5rem !important;
    }
    
    /* Enhanced metric cards with gradient backgrounds */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid rgba(0, 0, 0, 0.03);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* More vibrant metric values */
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(90deg, #1E88E5, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    
    /* Enhanced chart containers */
    .chart-container {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid rgba(0, 0, 0, 0.03);
    }
    
    /* Improved data tables */
    .data-table {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.03);
    }
    
    /* Enhanced header */
    .header-container {
        background: linear-gradient(90deg, #1E88E5 0%, #2196F3 50%, #42A5F5 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 6px 18px rgba(33, 150, 243, 0.2);
    }
    
    /* Enhance the sidebar */
    [data-testid="stSidebar"] {
        background-color: white;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    
    /* Better headings */
    h1, h2, h3, h4, h5 {
        color: #1e293b;
        font-weight: 700;
    }
    
    /* For those eligibility indicators with better colors */
    .eligible {
        color: #10b981;
        font-weight: bold;
        background: rgba(16, 185, 129, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    .not-eligible {
        color: #ef4444;
        font-weight: bold;
        background: rgba(239, 68, 68, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    .completion-high {
        color: #10b981;
        font-weight: bold;
        background: rgba(16, 185, 129, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    .completion-medium {
        color: #f59e0b;
        font-weight: bold;
        background: rgba(245, 158, 11, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    .completion-low {
        color: #ef4444;
        font-weight: bold;
        background: rgba(239, 68, 68, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    /* Remove padding from plotly charts */
    .js-plotly-plot .plotly {
        padding: 0 !important;
    }
    
    /* Improve the sidebar filter section */
    .sidebar .sidebar-content {
        background-color: white !important;
    }
    
    .sidebar h3 {
        font-size: 1.3rem;
        color: #4f46e5;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* More stylish buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1E88E5, #2196F3);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px 20px;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(33, 150, 243, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #2196F3, #42A5F5);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(33, 150, 243, 0.3);
    }
    
    /* Fix table styling */
    .stDataFrame {
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stDataFrame table {
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stDataFrame thead tr th {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        font-weight: 600;
        border-top: none !important;
        border-bottom: 2px solid #e2e8f0 !important;
        padding: 12px 15px !important;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #f8fafc !important;
    }
    
    .stDataFrame tbody tr td {
        border: none !important;
        padding: 12px 15px !important;
        color: #334155 !important;
        border-bottom: 1px solid #f1f5f9 !important;
    }
    
    /* Clean metric row styles */
    .metrics-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 30px;
    }
    
    .metric-container {
        flex: 1;
        min-width: 150px;
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .metric-container.purple {
        background-color: #f5f3ff;
    }
    
    .metric-container.pink {
        background-color: #fdf2f8;
    }
    
    .metric-header {
        font-size: 12px;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #4338ca;
        margin-bottom: 5px;
    }
    
    .metric-value.blue {
        color: #3b82f6;
    }
    
    .metric-value.purple {
        color: #8b5cf6;
    }
    
    /* Sidebar improvements */
    [data-testid="stSidebar"] {
        background-color: white;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar-section {
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .sidebar-header {
        font-size: 18px;
        font-weight: 600;
        color: #1E88E5;
        margin-bottom: 15px;
    }
    
    .sidebar-subheader {
        font-size: 14px;
        font-weight: 500;
        color: #64748b;
        margin: 10px 0 5px 0;
    }
    
    .sidebar-note {
        font-size: 12px;
        color: #94a3b8;
        font-style: italic;
        margin: 5px 0 10px 0;
        line-height: 1.4;
    }
    
    .sidebar-detail {
        margin: 8px 0;
        font-size: 14px;
    }
    
    .sidebar-detail strong {
        color: #334155;
        font-weight: 500;
    }
    
    .sidebar-detail a {
        color: #4f46e5;
        text-decoration: none;
    }
    
    .sidebar-detail a:hover {
        text-decoration: underline;
    }
    
    /* Logout button styling */
    .logout-button {
        background-color: #2196F3;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s;
        width: 100%;
        text-align: center;
    }
    
    .logout-button:hover {
        background-color: #1E88E5;
    }
    
    /* Date picker improvements */
    .date-input {
        margin-bottom: 10px;
    }
    
    /* Dropdown improvements */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
    
    /* Enhanced sidebar styles */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Make section headers more prominent */
    .sidebar-header {
        font-size: 18px;
        font-weight: 600;
        color: #1E88E5;
        margin: 20px 0 15px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #42A5F5;
    }
    
    /* Highlight interactive elements */
    .filter-highlight {
        background-color: #eff6ff;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 15px;
        border-left: 3px solid #3b82f6;
    }
    
    /* Improve date picker visibility */
    .date-label {
        font-weight: 500;
        color: #334155;
        margin-bottom: 5px;
    }
    
    /* Make dropdown more noticeable */
    .rep-dropdown {
        background-color: #f0f9ff;
        border-radius: 8px;
        padding: 10px;
        border-left: 3px solid #0ea5e9;
        margin-top: 10px;
    }
    
    /* Enhance logout button */
    .logout-button {
        background: linear-gradient(90deg, #6366f1, #4f46e5);
        color: white;
        padding: 10px 16px;
        border-radius: 6px;
        font-weight: 500;
        margin-top: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);
    }
    
    /* Improve rep details section */
    .rep-details {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Style accounts section */
    .accounts-section {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .account-item {
        padding: 8px 0;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
    }
    
    .account-item:last-child {
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)

# Function to load data
@st.cache_data
def load_data():
    try:
        # --- Load Real Transaction Data ---
        transaction_file = 'transaction_table.csv' # Assuming your file name
        transactions_df = pd.read_csv(transaction_file)
        #st.success(f"Loaded real transaction data from {transaction_file}")

        # --- Basic Data Cleaning & Preparation ---
        # Rename columns for consistency or use new names directly in functions
        # For clarity, let's rename to match the old structure where needed,
        # but ideally, update functions to use original names.
        # Here, we'll update functions instead.

        # Convert Date column
        transactions_df['TRAN_DT'] = pd.to_datetime(transactions_df['TRAN_DT'], errors='coerce')
        transactions_df = transactions_df.dropna(subset=['TRAN_DT', 'LCTN_ID', 'REP NAME', 'TRAN_AM']) # Drop essential missing data

        # Add Time Features
        transactions_df['Month'] = transactions_df['TRAN_DT'].dt.month_name()
        transactions_df['Quarter'] = 'Q' + transactions_df['TRAN_DT'].dt.quarter.astype(str)
        transactions_df['Year'] = transactions_df['TRAN_DT'].dt.year
        
        # Add TransactionVolume (assuming each row is one transaction)
        transactions_df['TransactionVolume'] = 1

        # --- Derive Accounts Data from Transactions ---
        # Get unique locations/accounts
        accounts_df = transactions_df[[
            'LCTN_ID', 'CHILD_LCTN_DBA_NM', 'REP NAME', 'CITY_NM', 'latitude', 'longitude', 'preprocessed_address' # Use 'preprocessed_address'
        ]].drop_duplicates(subset=['LCTN_ID']).copy()
        
        # Rename for compatibility with existing functions (will update functions later)
        accounts_df = accounts_df.rename(columns={
            'LCTN_ID': 'AccountID',
            'CHILD_LCTN_DBA_NM': 'AccountName',
            'REP NAME': 'RepID', # Using Rep Name as RepID here
            'CITY_NM': 'CityName',
            'preprocessed_address': 'full_address' # Map preprocessed to full_address
            # latitude, longitude names are kept
        })
        # Fill any NaNs introduced if CHILD_LCTN_DBA_NM was sometimes missing
        accounts_df['AccountName'] = accounts_df['AccountName'].fillna('Unknown Account')
        accounts_df['full_address'] = accounts_df['full_address'].fillna('Address Unavailable')

        # --- Derive Sales Reps Data from Transactions ---
        sales_reps_df = transactions_df[['REP NAME']].drop_duplicates().copy()
        sales_reps_df = sales_reps_df.rename(columns={'REP NAME': 'RepID'})
        # Assuming RepName is the same as RepID (the name string)
        sales_reps_df['RepName'] = sales_reps_df['RepID']

        # --- Create Data Dictionary ---
        data = {'sales_reps': sales_reps_df, 'accounts': accounts_df, 'transactions': transactions_df}

        # --- Assigned Accounts (Maps accounts to their designated rep) ---
        # This is implicitly defined in accounts_df already
        data['assigned_accounts'] = data['accounts'][['AccountID', 'RepID']].copy()

        # --- Generate sales_targets (Keep placeholder or load real targets) ---
        # Using placeholder for now, replace if you have real target data
        rep_ids = data['sales_reps']['RepID'].tolist()
        sales_targets_list = []
        np.random.seed(42)
        for rep_id in rep_ids:
            bonus_threshold = np.random.randint(100000, 500000) # Placeholder target
            eligibility_prob = 0.2 + (hash(rep_id) % 6) / 10.0
            bonus_eligibility = np.random.choice([True, False], p=[eligibility_prob, 1-eligibility_prob])
            sales_targets_list.append({
                'RepID': rep_id, # RepID is the Rep Name string
                'BonusThreshold': bonus_threshold,
                'Bonus_Eligibility': bonus_eligibility
            })
        data['sales_targets'] = pd.DataFrame(sales_targets_list)
        
        # --- Create territory_performance from REAL data ---
        # Use the original transaction_table columns for aggregation
        territory_agg = transactions_df.groupby(['CITY_NM']).agg(
            Total_Processing=('TRAN_AM', 'sum'),
            Total_Transactions=('TransactionVolume', 'sum'),
            latitude=('latitude', 'first'), # Take first available lat/lon/address per city
            longitude=('longitude', 'first'),
            full_address=('preprocessed_address', 'first') # Use preprocessed address
        ).reset_index()
        
        # Rename CityName to 'city' for map function compatibility
        territory_agg = territory_agg.rename(columns={'CITY_NM': 'city'})
        
        # Ensure required columns exist and handle NAs
        required_terr_cols = ['city', 'Total_Processing', 'Total_Transactions', 'latitude', 'longitude', 'full_address']
        for col in required_terr_cols:
            if col not in territory_agg.columns:
                 territory_agg[col] = np.nan # Add missing columns if needed

        territory_agg['city'] = territory_agg['city'].astype(str).fillna('Unknown')
        territory_agg['full_address'] = territory_agg['full_address'].astype(str).fillna('Address Unavailable')
        territory_agg['latitude'] = pd.to_numeric(territory_agg['latitude'], errors='coerce').fillna(0)
        territory_agg['longitude'] = pd.to_numeric(territory_agg['longitude'], errors='coerce').fillna(0)
        territory_agg['Total_Processing'] = pd.to_numeric(territory_agg['Total_Processing'], errors='coerce').fillna(0)
        territory_agg['Total_Transactions'] = pd.to_numeric(territory_agg['Total_Transactions'], errors='coerce').fillna(0)

        data['territory_performance'] = territory_agg

        # REMOVED: enhance_territory_data call as enhancement is done above

        # --- Load Performance Data (Keep as is for now) ---
        try:
            performance_data = pd.read_csv("performance_data.csv").fillna(0)
            performance_data['Date'] = pd.to_datetime(performance_data['Date'], errors='coerce')
            performance_data = performance_data.dropna(subset=['Date'])
            performance_data['Month'] = performance_data['Date'].dt.month # Keep numeric month
            performance_data['Year'] = performance_data['Date'].dt.year
            data['performance_data'] = performance_data
        except FileNotFoundError:
            st.warning("performance_data.csv not found. Activity charts will not be available.")
            data['performance_data'] = pd.DataFrame() # Empty DataFrame
        except Exception as e:
            st.error(f"Error loading performance_data.csv: {e}")
            data['performance_data'] = pd.DataFrame()

        
        return data

    except FileNotFoundError:
        st.error(f"Error: '{transaction_file}' not found. Please ensure the transaction data file exists.")
        return None
    except Exception as e:
        st.error(f"Error loading or processing data: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None

def enhance_territory_data(data):
    # This function might still be useful for future enhancements or checks
    # For now, the core logic is integrated into load_data
    required_cols = ['city', 'Total_Processing', 'Total_Transactions', 'latitude', 'longitude', 'full_address']
    if 'territory_performance' not in data:
        data['territory_performance'] = pd.DataFrame(columns=required_cols)
        return data

    # Ensure numeric columns are numeric
    for col in ['latitude', 'longitude', 'Total_Processing', 'Total_Transactions']:
         if col in data['territory_performance'].columns:
             data['territory_performance'][col] = pd.to_numeric(data['territory_performance'][col], errors='coerce').fillna(0).astype(float)
         else:
             data['territory_performance'][col] = 0.0

    # Ensure string columns are string
    for col in ['city', 'full_address']:
         if col in data['territory_performance'].columns:
             fill_val = 'Unknown' if col == 'city' else 'Address Unavailable'
             data['territory_performance'][col] = data['territory_performance'][col].astype(str).fillna(fill_val)
         else:
              fill_val = 'Unknown' if col == 'city' else 'Address Unavailable'
              data['territory_performance'][col] = fill_val

    return data

def calculate_rep_metrics(data, rep_id, start_date, end_date):
    """Calculate metrics for a specific sales rep"""
    # Get rep's accounts (AccountID comes from the accounts_df where LCTN_ID was renamed)
    rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id]['AccountID'].tolist()
    
    # Filter transactions using LCTN_ID and TRAN_DT from the original transactions_df
    filtered_transactions = data['transactions'][
        (data['transactions']['LCTN_ID'].isin(rep_accounts)) & # Use LCTN_ID here
        (data['transactions']['TRAN_DT'] >= start_date) &      # Use TRAN_DT here
        (data['transactions']['TRAN_DT'] <= end_date)
    ]
    
    # Calculate metrics using TRAN_AM and TransactionVolume
    total_processed = filtered_transactions['TRAN_AM'].sum() # Use TRAN_AM here
    total_volume = filtered_transactions['TransactionVolume'].sum() # Use TransactionVolume here
    
    # Get YTD goal from sales_targets (RepID here is the REP NAME string)
    target_info = data['sales_targets'][data['sales_targets']['RepID'] == rep_id]
    ytd_goal = target_info['BonusThreshold'].iloc[0] if not target_info.empty else 0
    
    # Calculate completion percentage (as a percentage, not a decimal)
    completion_percentage = round((total_processed / ytd_goal) * 100, 2) if ytd_goal > 0 else 0
    
    # Determine bonus eligibility based on real data (or keep placeholder logic)
    bonus_eligibility_status = completion_percentage >= 100 # Example eligibility logic
    
    # Optional: Get pre-defined eligibility from sales_targets if it exists and is reliable
    # if not target_info.empty and 'Bonus_Eligibility' in target_info.columns:
    #     bonus_eligibility_status = target_info['Bonus_Eligibility'].iloc[0]
    
    return {
        'total_processed': total_processed,
        'total_volume': total_volume,
        'ytd_goal': ytd_goal,
        'completion_percentage': completion_percentage,
        'bonus_eligibility': bonus_eligibility_status # Use the derived status
    }

def create_time_series_chart(data, rep_id, start_date, end_date):
    # Get rep's accounts (AccountID from accounts_df)
    rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id]['AccountID'].tolist()
    
    # Filter transactions using LCTN_ID and TRAN_DT
    rep_transactions = data['transactions'][
        (data['transactions']['LCTN_ID'].isin(rep_accounts)) &  # Use LCTN_ID instead of AccountID
        (data['transactions']['TRAN_DT'] >= start_date) &      # Use TRAN_DT instead of TransactionDate
        (data['transactions']['TRAN_DT'] <= end_date)
    ]
    
    # Group by TRAN_DT and sum TRAN_AM
    daily_amounts = rep_transactions.groupby('TRAN_DT')['TRAN_AM'].sum().reset_index() # Use TRAN_DT, TRAN_AM
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_amounts['TRAN_DT'], # Use TRAN_DT
        y=daily_amounts['TRAN_AM'], # Use TRAN_AM
        mode='lines',
        fill='tozeroy',
        line=dict(color='#2196F3', width=2),
        fillcolor='rgba(33, 150, 243, 0.2)'
    ))
    fig.update_layout(
        title={
            'text': 'Processing Amount Over Time',
            'font': {
                'family': 'Roboto, sans-serif',
                'size': 18,
                'color': '#1e293b'
            },
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title='Processing Amount ($)',
        margin=dict(l=0, r=0, t=40, b=0),
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.05)', 
            zerolinecolor='rgba(0,0,0,0.1)',
            title_font={'color': '#64748b'}
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)', 
            zerolinecolor='rgba(0,0,0,0.1)',
            title_font={'color': '#64748b'}
        ),
        hovermode='x unified',
        font={'family': 'Roboto, sans-serif', 'color': '#334155'}
    )
    return fig

def create_map_visualization(data, rep_id, start_date, end_date):
    """Create a map visualization showing territory performance for a specific rep and date range"""
    # Get rep's accounts (AccountID from accounts_df)
    rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id]['AccountID'].tolist()

    # Filter transactions for the rep AND the date range
    filtered_transactions = data['transactions'][
        (data['transactions']['LCTN_ID'].isin(rep_accounts)) &
        (data['transactions']['TRAN_DT'] >= start_date) &
        (data['transactions']['TRAN_DT'] <= end_date)
    ].copy()

    # If no transactions in the period for this rep, return an empty map
    if filtered_transactions.empty:
        # st.info(f"No transaction data for rep {rep_id} in the selected period.") # Optional info message
        fig = go.Figure() # Start with base map structure even if empty
        fig.add_trace(go.Choropleth(
            locationmode='USA-states',
            locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                       'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                       'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                       'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                       'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
            z=[0]*50,
            colorscale=[[0, 'rgba(240, 240, 240, 0.8)'], [1, 'rgba(240, 240, 240, 0.8)']],
            showscale=False,
            marker_line_color='white',
            marker_line_width=0.5
        ))
        fig.update_layout( # Apply basic layout
            title={
                'text': 'Territory Performance (Selected Period)',
                'font': {'family': 'Roboto, sans-serif', 'size': 18, 'color': '#1e293b'},
                'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
            },
            showlegend=False,
            geo=dict(scope='usa', projection_type='albers usa', showland=True, landcolor='rgb(250, 250, 250)', countrycolor='rgb(204, 204, 204)', bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=40, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig # Return the empty-looking map

    # Aggregate the filtered transactions by City
    rep_territory = filtered_transactions.groupby('CITY_NM').agg(
        Total_Processing=('TRAN_AM', 'sum'),
        Total_Transactions=('TransactionVolume', 'sum'),
        latitude=('latitude', 'first'),
        longitude=('longitude', 'first'),
        full_address=('preprocessed_address', 'first')
    ).reset_index()

    # Rename city column for consistency
    rep_territory = rep_territory.rename(columns={'CITY_NM': 'city'})

    # Ensure required columns exist and handle NAs (similar to load_data logic)
    required_map_cols = ['city', 'Total_Processing', 'Total_Transactions', 'latitude', 'longitude', 'full_address']
    for col in required_map_cols:
        if col not in rep_territory.columns:
            rep_territory[col] = np.nan

    rep_territory['city'] = rep_territory['city'].astype(str).fillna('Unknown')
    rep_territory['full_address'] = rep_territory['full_address'].astype(str).fillna('Address Unavailable')
    rep_territory['latitude'] = pd.to_numeric(rep_territory['latitude'], errors='coerce').fillna(0)
    rep_territory['longitude'] = pd.to_numeric(rep_territory['longitude'], errors='coerce').fillna(0)
    rep_territory['Total_Processing'] = pd.to_numeric(rep_territory['Total_Processing'], errors='coerce').fillna(0)
    rep_territory['Total_Transactions'] = pd.to_numeric(rep_territory['Total_Transactions'], errors='coerce').fillna(0)

    # --- Create Base Map ---
    fig = go.Figure()
    fig.add_trace(go.Choropleth(
        locationmode='USA-states',
        locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                   'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                   'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                   'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                   'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
        z=[0]*50,
        colorscale=[[0, 'rgba(240, 240, 240, 0.8)'], [1, 'rgba(240, 240, 240, 0.8)']],
        showscale=False,
        marker_line_color='white',
        marker_line_width=0.5
    ))

    # --- Add Bubbles using dynamically aggregated data ---
    if not rep_territory.empty:
        # Filter out entries with 0 lat/lon before plotting
        rep_territory_plot = rep_territory[
            (rep_territory['latitude'] != 0) & (rep_territory['longitude'] != 0)
        ].copy()

        if not rep_territory_plot.empty:
            max_amount = rep_territory_plot['Total_Processing'].max() if rep_territory_plot['Total_Processing'].max() > 0 else 1
            min_size = 15
            max_size = 50
            # Calculate sizes based on the filtered data
            sizes = min_size + (rep_territory_plot['Total_Processing'] / max_amount) * (max_size - min_size)

            fig.add_trace(go.Scattergeo(
                locationmode='USA-states',
                lon=rep_territory_plot['longitude'],
                lat=rep_territory_plot['latitude'],
                # Include full address in hover text
                text=rep_territory_plot.apply(
                    lambda row: f"<b>{row['city']}</b><br>Total: ${row['Total_Processing']:,.2f}<br>Transactions: {row['Total_Transactions']}<br>Address: {row['full_address']}",
                    axis=1
                ),
                mode='markers',
                marker=dict(
                    size=sizes,
                    color='#818cf8',
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                name='Territory Performance',
                hoverinfo='text'
            ))

    # Update the geo layout properties
    fig.update_layout(
        title={
            'text': 'Territory Performance (Selected Period)', # Updated title
            'font': {
                'family': 'Roboto, sans-serif',
                'size': 18, # Adjusted size slightly
                'color': '#1e293b'
            },
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(250, 250, 250)',
            countrycolor='rgb(204, 204, 204)',
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            showsubunits=True,
            subunitcolor='rgb(230, 230, 230)',
            center=dict(lat=39.5, lon=-98.5),
            projection_scale=7.0,
            bgcolor='rgba(0,0,0,0)' # Added transparent background
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

def create_transaction_table(data, rep_id, start_date, end_date):
    """Create transaction details table for a specific rep, using Grandparent as Account Name"""
    # Get rep's accounts - we still need this to filter transactions by rep
    rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id]['AccountID'].tolist()

    # Filter transactions using LCTN_ID (to get rep's transactions) and TRAN_DT
    rep_transactions = data['transactions'][
        (data['transactions']['LCTN_ID'].isin(rep_accounts)) & # Use LCTN_ID instead of AccountID
        (data['transactions']['TRAN_DT'] >= start_date) &      # Use TRAN_DT instead of TransactionDate
        (data['transactions']['TRAN_DT'] <= end_date)
    ].copy() # Add .copy()

    # If no transactions, return empty dataframe
    if rep_transactions.empty:
        return pd.DataFrame(columns=[
            'AccountID', 'AccountName', 'RepName', 'Year', 'Quarter', 'Month',
            'Sum of ProcessingAmount', 'Count of Transactions'
        ])

    # REMOVED: Merge with accounts details - we'll get names directly

    # Ensure needed columns exist and fill NA
    required_cols = ['LCTN_ID', 'GRANDPARENT_CORP_DBA_NM', 'REP NAME', 'Year', 'Quarter', 'Month', 'TRAN_AM', 'TransactionVolume']
    for col in required_cols:
         if col not in rep_transactions.columns:
             # Use appropriate fill for missing columns
             fill_value = 'N/A' if col == 'GRANDPARENT_CORP_DBA_NM' else ('Unknown Rep' if col == 'REP NAME' else ('Unknown' if col in ['Year', 'Quarter', 'Month'] else 0))
             rep_transactions[col] = fill_value
         else:
             # Fill missing values specifically for these columns
             if col == 'REP NAME':
                 rep_transactions[col] = rep_transactions[col].fillna('Unknown Rep')
             elif col == 'GRANDPARENT_CORP_DBA_NM':
                 rep_transactions[col] = rep_transactions[col].fillna('N/A')
             # Keep existing logic for other columns like Year, Quarter, Month if they have it
             elif col in ['TRAN_AM', 'TransactionVolume']:
                 rep_transactions[col] = rep_transactions[col].fillna(0)
             # Add handling for time columns if needed, though they are added earlier
             elif col in ['Year', 'Quarter', 'Month']:
                 rep_transactions[col] = rep_transactions[col].fillna('Unknown')


    # Group by required fields, using GRANDPARENT name
    grouped_transactions = rep_transactions.groupby(
        ['LCTN_ID', 'GRANDPARENT_CORP_DBA_NM', 'REP NAME', 'Year', 'Quarter', 'Month'] # Group by Grandparent
    ).agg(
        TRAN_AM=('TRAN_AM', 'sum'),           # Use named agg
        TransactionVolume=('TransactionVolume', 'sum')
    ).reset_index()

    # Rename for display
    grouped_transactions = grouped_transactions.rename(columns={
        'LCTN_ID': 'AccountID',               # Keep original AccountID (LCTN_ID)
        'GRANDPARENT_CORP_DBA_NM': 'AccountName', # Display Grandparent as AccountName
        'REP NAME': 'RepName',                # Use rep name from transaction
        'TRAN_AM': 'Sum of ProcessingAmount',
        'TransactionVolume': 'Count of Transactions'
    })

    # Format currency
    grouped_transactions['Sum of ProcessingAmount'] = grouped_transactions['Sum of ProcessingAmount'].apply(
        lambda x: f"${x:,.2f}"
    )

    # Select and order columns
    final_cols = ['AccountID', 'AccountName', 'RepName', 'Year', 'Quarter', 'Month', 'Sum of ProcessingAmount', 'Count of Transactions']
    return grouped_transactions[final_cols]

def create_volume_time_series_chart(data, rep_id, start_date, end_date):
    # Get rep's accounts
    rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id]['AccountID'].tolist()
    
    # Filter transactions using LCTN_ID and TRAN_DT
    rep_transactions = data['transactions'][
        (data['transactions']['LCTN_ID'].isin(rep_accounts)) &  # Use LCTN_ID instead of AccountID
        (data['transactions']['TRAN_DT'] >= start_date) &      # Use TRAN_DT instead of TransactionDate
        (data['transactions']['TRAN_DT'] <= end_date)
    ]
    
    # Group by TRAN_DT and sum TransactionVolume
    daily_volumes = rep_transactions.groupby('TRAN_DT')['TransactionVolume'].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_volumes['TRAN_DT'],  # Use TRAN_DT instead of TransactionDate
        y=daily_volumes['TransactionVolume'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#2196F3', width=2),
        fillcolor='rgba(33, 150, 243, 0.2)'
    ))
    
    # Rest of the function stays the same
    fig.update_layout(
        title={
            'text': 'Transaction Volume Over Time',
            'font': {
                'family': 'Roboto, sans-serif',
                'size': 18,
                'color': '#1e293b'
            },
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title='Transaction Volume',
        margin=dict(l=0, r=0, t=40, b=0),
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.05)', 
            zerolinecolor='rgba(0,0,0,0.1)',
            title_font={'color': '#64748b'}
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)', 
            zerolinecolor='rgba(0,0,0,0.1)',
            title_font={'color': '#64748b'}
        ),
        hovermode='x unified',
        font={'family': 'Roboto, sans-serif', 'color': '#334155'}
    )
    return fig

def create_compensation_model(data, rep_id):
    """Create an enhanced compensation model display with split tables and visualizations"""
    # Get rep details
    rep_details = data['sales_reps'][data['sales_reps']['RepID'] == rep_id].iloc[0]
    rep_name = rep_details['RepName']
    
    # Get target info
    target_info = data['sales_targets'][data['sales_targets']['RepID'] == rep_id]
    if not target_info.empty:
        bonus_threshold = target_info.iloc[0]['BonusThreshold']
        bonus_eligibility = target_info.iloc[0]['Bonus_Eligibility']
    else:
        bonus_threshold = 0
        bonus_eligibility = False
    
    # Generate random monthly targets and actuals for visualization
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_targets = [bonus_threshold/12 for _ in range(12)]
    
    # Make actuals follow a realistic pattern (higher in later months)
    monthly_actuals = []
    for i in range(12):
        # Increase likelihood of meeting targets in later months
        factor = 0.5 + (i * 0.05)  # Starts at 50% of target, increases by 5% each month
        monthly_actuals.append(monthly_targets[i] * factor * random.uniform(0.8, 1.2))
    
    # Calculate cumulative values for YTD comparison
    cumulative_targets = [sum(monthly_targets[:i+1]) for i in range(12)]
    cumulative_actuals = [sum(monthly_actuals[:i+1]) for i in range(12)]
    
    # Calculate monthly commission rates (random for this example)
    base_commission_rates = [random.uniform(1.0, 2.5) for _ in range(12)]
    bonus_commission_rates = [rate + random.uniform(0.5, 1.5) for rate in base_commission_rates]
    
    # Calculate estimated commissions
    monthly_base_commissions = [monthly_actuals[i] * (base_commission_rates[i]/100) for i in range(12)]
    monthly_bonus_commissions = [monthly_actuals[i] * (bonus_commission_rates[i]/100) if cumulative_actuals[i] >= cumulative_targets[i] else 0 for i in range(12)]
    total_commissions = [monthly_base_commissions[i] + monthly_bonus_commissions[i] for i in range(12)]
    
    # Determine color for YTD completion
    ytd_completion_color = "#047857" if (cumulative_actuals[5]/cumulative_targets[5]) >= 1 else "#b91c1c"
    bonus_eligibility_color = "#047857" if bonus_eligibility else "#b91c1c"
    
    # Create the HTML for the compensation model
    html = f"""
    <div style="font-family: 'Inter', sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background-color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h2 style="color: #111827; margin: 0;">Compensation Model: {rep_name}</h2>
            <div style="background-color: #f3f4f6; padding: 10px 15px; border-radius: 8px;">
                <span style="font-weight: 500; color: #374151;">Annual Bonus Threshold:</span>
                <span style="font-weight: 600; color: #111827; margin-left: 5px;">${bonus_threshold:,.2f}</span>
            </div>
        </div>
        
        <div style="display: flex; gap: 20px; margin-bottom: 30px;">
            <div style="flex: 1; background-color: #f9fafb; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h3 style="color: #1E88E5; margin-top: 0; margin-bottom: 15px;">Performance Summary</h3>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #6b7280;">YTD Target:</span>
                    <span style="font-weight: 600; color: #111827;">${cumulative_targets[5]:,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #6b7280;">YTD Actual:</span>
                    <span style="font-weight: 600; color: #111827;">${cumulative_actuals[5]:,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #6b7280;">YTD Completion:</span>
                    <span style="font-weight: 600; color: {ytd_completion_color};">
                        ${(cumulative_actuals[5]/cumulative_targets[5])*100:.1f}%
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #6b7280;">Bonus Eligibility:</span>
                    <span style="font-weight: 600; color: {bonus_eligibility_color};">
                        ${bonus_eligibility and 'Eligible' or 'Not Eligible'}
                    </span>
                </div>
            </div>
            
            <div style="flex: 2; background-color: #f9fafb; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h3 style="color: #1E88E5; margin-top: 0; margin-bottom: 15px;">YTD Commission Summary</h3>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #6b7280;">Base Commission:</span>
                    <span style="font-weight: 600; color: #111827;">${sum(monthly_base_commissions):,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #6b7280;">Bonus Commission:</span>
                    <span style="font-weight: 600; color: #111827;">${sum(monthly_bonus_commissions):,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px; border-top: 1px solid #e5e7eb; padding-top: 10px;">
                    <span style="color: #6b7280; font-weight: 500;">Total Commission:</span>
                    <span style="font-weight: 700; color: #1E88E5; font-size: 1.1em;">${sum(total_commissions):,.2f}</span>
                </div>
            </div>
        </div>
        
        <div style="margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="color: #111827; margin: 0;">Monthly Performance (First Half)</h3>
                <div style="background-color: #E3F2FD; color: #1E88E5; padding: 5px 10px; border-radius: 4px; font-size: 14px; font-weight: 500;">
                    January - June 2023
                </div>
            </div>
            
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                    <thead>
                        <tr style="background-color: #f3f4f6; border-bottom: 2px solid #e5e7eb;">
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Month</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Target</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Actual</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Completion %</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Base Rate</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Bonus Rate</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Base Commission</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Bonus Commission</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Add rows for first 6 months
    for i in range(6):
        completion_pct = (monthly_actuals[i] / monthly_targets[i]) * 100
        row_class = "background-color: #f8fafc;" if i % 2 == 1 else ""
        completion_color = "#047857" if completion_pct >= 100 else "#b91c1c"
        
        html += f"""
                        <tr style="{row_class} border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 10px 15px; font-weight: 500;">{months[i]}</td>
                            <td style="padding: 10px 15px;">${monthly_targets[i]:,.2f}</td>
                            <td style="padding: 10px 15px;">${monthly_actuals[i]:,.2f}</td>
                            <td style="padding: 10px 15px; color: {completion_color};">{completion_pct:.1f}%</td>
                            <td style="padding: 10px 15px;">{base_commission_rates[i]:.2f}%</td>
                            <td style="padding: 10px 15px;">{bonus_commission_rates[i]:.2f}%</td>
                            <td style="padding: 10px 15px;">${monthly_base_commissions[i]:,.2f}</td>
                            <td style="padding: 10px 15px;">${monthly_bonus_commissions[i]:,.2f}</td>
                            <td style="padding: 10px 15px; font-weight: 600;">${total_commissions[i]:,.2f}</td>
                        </tr>
        """
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <div style="margin-bottom: 30px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="color: #111827; margin: 0;">Monthly Performance (Second Half)</h3>
                <div style="background-color: #E3F2FD; color: #1E88E5; padding: 5px 10px; border-radius: 4px; font-size: 14px; font-weight: 500;">
                    July - December 2023
                </div>
            </div>
            
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                    <thead>
                        <tr style="background-color: #f3f4f6; border-bottom: 2px solid #e5e7eb;">
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Month</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Target</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Actual</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Completion %</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Base Rate</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Bonus Rate</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Base Commission</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Bonus Commission</th>
                            <th style="padding: 12px 15px; font-weight: 600; color: #374151;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Add rows for last 6 months
    for i in range(6, 12):
        completion_pct = (monthly_actuals[i] / monthly_targets[i]) * 100
        row_class = "background-color: #f8fafc;" if i % 2 == 1 else ""
        completion_color = "#047857" if completion_pct >= 100 else "#b91c1c"
        
        html += f"""
                        <tr style="{row_class} border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 10px 15px; font-weight: 500;">{months[i]}</td>
                            <td style="padding: 10px 15px;">${monthly_targets[i]:,.2f}</td>
                            <td style="padding: 10px 15px;">${monthly_actuals[i]:,.2f}</td>
                            <td style="padding: 10px 15px; color: {completion_color};">{completion_pct:.1f}%</td>
                            <td style="padding: 10px 15px;">{base_commission_rates[i]:.2f}%</td>
                            <td style="padding: 10px 15px;">{bonus_commission_rates[i]:.2f}%</td>
                            <td style="padding: 10px 15px;">${monthly_base_commissions[i]:,.2f}</td>
                            <td style="padding: 10px 15px;">${monthly_bonus_commissions[i]:,.2f}</td>
                            <td style="padding: 10px 15px; font-weight: 600;">${total_commissions[i]:,.2f}</td>
                        </tr>
        """
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <div style="margin-bottom: 30px;">
            <h3 style="color: #111827; margin-bottom: 15px;">Performance Trends</h3>
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1; height: 300px; background-color: #f9fafb; border-radius: 8px; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div id="target-vs-actual-chart"></div>
                </div>
                <div style="flex: 1; height: 300px; background-color: #f9fafb; border-radius: 8px; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div id="commission-breakdown-chart"></div>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 30px; text-align: center; color: #6b7280; font-size: 12px;">
            © 2025 Sky Systemz. All rights reserved.
        </div>
        
        <!-- Include Plotly.js -->
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        
        <script>
            // Target vs Actual Chart
            var targetVsActualData = [
                {
                    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    y: [${', '.join(str(x) for x in monthly_targets)}],
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Target',
                    line: {color: '#6366f1', width: 3},
                    marker: {size: 8}
                },
                {
                    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    y: [${', '.join(str(x) for x in monthly_actuals)}],
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Actual',
                    line: {color: '#f97316', width: 3},
                    marker: {size: 8}
                }
            ];
            
            var targetVsActualLayout = {
                title: 'Monthly Target vs. Actual',
                font: {family: 'Inter, sans-serif'},
                margin: {l: 50, r: 20, t: 40, b: 40},
                legend: {orientation: 'h', y: 1.1},
                plot_bgcolor: '#f9fafb',
                paper_bgcolor: '#f9fafb',
                xaxis: {gridcolor: '#e5e7eb'},
                yaxis: {
                    gridcolor: '#e5e7eb',
                    title: 'Amount ($)',
                    tickformat: '$,.0f'
                }
            };
            
            Plotly.newPlot('target-vs-actual-chart', targetVsActualData, targetVsActualLayout, {responsive: true});
            
            // Commission Breakdown Chart
            var commissionData = [
                {
                    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    y: [${', '.join(str(x) for x in monthly_base_commissions)}],
                    type: 'bar',
                    name: 'Base Commission',
                    marker: {color: '#6366f1'}
                },
                {
                    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    y: [${', '.join(str(x) for x in monthly_bonus_commissions)}],
                    type: 'bar',
                    name: 'Bonus Commission',
                    marker: {color: '#10b981'}
                }
            ];
            
            var commissionLayout = {
                title: 'Monthly Commission Breakdown',
                font: {family: 'Inter, sans-serif'},
                barmode: 'stack',
                margin: {l: 50, r: 20, t: 40, b: 40},
                legend: {orientation: 'h', y: 1.1},
                plot_bgcolor: '#f9fafb',
                paper_bgcolor: '#f9fafb',
                xaxis: {gridcolor: '#e5e7eb'},
                yaxis: {
                    gridcolor: '#e5e7eb',
                    title: 'Commission ($)',
                    tickformat: '$,.0f'
                }
            };
            
            Plotly.newPlot('commission-breakdown-chart', commissionData, commissionLayout, {responsive: true});
        </script>
    </div>
    """
    
    return html

def create_revenue_comparison(data, start_date, end_date): # Renamed function
    """Create a bar chart comparing revenue for top sales reps within a date range"""
    # Filter transactions by date first
    transactions = data['transactions'][
        (data['transactions']['TRAN_DT'] >= start_date) &
        (data['transactions']['TRAN_DT'] <= end_date)
    ].copy()

    # Get accounts data
    accounts = data['accounts'].copy() # Should have AccountID (renamed LCTN_ID), RepID (name)

    # --- Ensure the merge uses correct keys ---
    # Join transactions (left) with accounts (right)
    transactions_with_rep = transactions.merge(
        accounts[['AccountID', 'RepID']], # Select only needed columns from accounts
        left_on='LCTN_ID',               # Key from left DataFrame (transactions)
        right_on='AccountID',              # Key from right DataFrame (accounts)
        how='left'
    )

    # RepName is now in transactions_with_rep as 'RepID' from the merge
    # Handle potential missing matches from the merge
    transactions_with_rep['RepID'] = transactions_with_rep['RepID'].fillna('Unknown Rep')

    # Group by RepID (the name string) and calculate sums using TRAN_AM
    rep_performance = transactions_with_rep.groupby('RepID').agg({ # Group by RepID (name)
        'TRAN_AM': 'sum',           # Use TRAN_AM
        # 'TransactionVolume': 'sum' # Volume not needed for this chart
    }).reset_index()

    # Rename RepID to RepName for display and TRAN_AM to ProcessingAmount
    rep_performance = rep_performance.rename(columns={'RepID': 'RepName', 'TRAN_AM': 'ProcessingAmount'})

    # REMOVED: Estimated Profit calculation

    # Sort by ProcessingAmount and take top 5
    rep_performance = rep_performance.sort_values('ProcessingAmount', ascending=False).head(5)

    # Create the figure
    fig = go.Figure()

    # Add ProcessingAmount bars
    fig.add_trace(go.Bar(
        y=rep_performance['RepName'],
        x=rep_performance['ProcessingAmount'],
        name='Sum of ProcessingAmount', # Keep name for clarity if legend were shown
        orientation='h',
        marker=dict(color='rgba(79, 70, 229, 0.9)'), # Use the darker color now
        hovertemplate='%{y}: $%{x:,.2f}<extra></extra>'
    ))

    # REMOVED: EstimatedProfit bars trace

    # Update layout
    fig.update_layout(
        title={
            'text': 'Top Representatives by Processing Amount', # Updated title
            'font': {
                'family': 'Roboto, sans-serif',
                'size': 18,
                'color': '#1e293b'
            },
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Processing Amount ($)',
        yaxis_title=None, # Remove y-axis title if desired
        # barmode='group', # No longer grouped
        margin=dict(l=0, r=0, t=40, b=0),
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.05)', separatethousands=True, tickprefix='$'), # Format x-axis
        # legend=dict( # Legend not really needed for single bar type
        #     orientation='h',
        #     yanchor='bottom',
        #     y=1.02,
        #     xanchor='right',
        #     x=1,
        #     font={'size': 12, 'color': '#64748b'}
        # ),
        showlegend=False, # Hide legend
        font={'family': 'Roboto, sans-serif', 'color': '#334155'}
    )

    return fig

def create_processing_by_location_map(data, start_date, end_date): # Renamed function
    """Create a map showing processing amount by location (City) and total transactions for the selected period"""
    # Filter transactions by date first
    filtered_transactions = data['transactions'][
        (data['transactions']['TRAN_DT'] >= start_date) &
        (data['transactions']['TRAN_DT'] <= end_date)
    ].copy()

    # If no transactions in the period, return an empty map
    if filtered_transactions.empty:
        fig = go.Figure() # Start with base map structure even if empty
        fig.add_trace(go.Choropleth(
            locationmode='USA-states', locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], z=[0]*50, colorscale=[[0, 'rgba(240, 240, 240, 0.8)'], [1, 'rgba(240, 240, 240, 0.8)']], showscale=False, marker_line_color='white', marker_line_width=0.5
        ))
        fig.update_layout( # Apply basic layout
            title={'text': 'Processing Amount by Location', 'font': {'family': 'Roboto, sans-serif', 'size': 18, 'color': '#1e293b'}, 'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
            showlegend=False, geo=dict(scope='usa', projection_type='albers usa', showland=True, landcolor='rgb(250, 250, 250)', countrycolor='rgb(204, 204, 204)', bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=40, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    # Aggregate filtered transactions by City
    territory_data = filtered_transactions.groupby('CITY_NM').agg(
        Total_Processing=('TRAN_AM', 'sum'),
        Total_Transactions=('TransactionVolume', 'sum'),
        latitude=('latitude', 'first'),
        longitude=('longitude', 'first'),
        full_address=('preprocessed_address', 'first')
    ).reset_index()

    # Rename city column
    territory_data = territory_data.rename(columns={'CITY_NM': 'city'})

    # Data Cleaning and Preparation (similar to load_data)
    required_map_cols = ['city', 'Total_Processing', 'Total_Transactions', 'latitude', 'longitude', 'full_address']
    for col in required_map_cols:
        if col not in territory_data.columns: territory_data[col] = np.nan
    territory_data['city'] = territory_data['city'].astype(str).fillna('Unknown')
    territory_data['full_address'] = territory_data['full_address'].astype(str).fillna('Address Unavailable')
    territory_data['latitude'] = pd.to_numeric(territory_data['latitude'], errors='coerce')
    territory_data['longitude'] = pd.to_numeric(territory_data['longitude'], errors='coerce')
    territory_data['Total_Processing'] = pd.to_numeric(territory_data['Total_Processing'], errors='coerce').fillna(0)
    territory_data['Total_Transactions'] = pd.to_numeric(territory_data['Total_Transactions'], errors='coerce').fillna(0)

    # REMOVED: Estimated Profit calculation

    # Create the figure
    fig = go.Figure()

    # Add base map
    fig.add_trace(go.Choropleth(
        locationmode='USA-states', locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], z=[0]*50, colorscale=[[0, 'rgba(240, 240, 240, 0.8)'], [1, 'rgba(240, 240, 240, 0.8)']], showscale=False, marker_line_color='white', marker_line_width=0.5
    ))

    # Add bubbles for each city
    territory_data_plot = territory_data[
        territory_data['latitude'].notna() & territory_data['longitude'].notna() &
        (territory_data['latitude'] != 0) & (territory_data['longitude'] != 0)
    ].copy()

    if not territory_data_plot.empty:
        # Calculate bubble size based on Total_Processing
        max_processing = territory_data_plot['Total_Processing'].max() if territory_data_plot['Total_Processing'].max() > 0 else 1
        min_size = 15
        max_size = 50
        territory_data_plot['size'] = min_size + (territory_data_plot['Total_Processing'] / max_processing) * (max_size - min_size)

        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=territory_data_plot['longitude'],
            lat=territory_data_plot['latitude'],
            # Update hover text to show Total Processing
            text=territory_data_plot.apply(
                lambda row: f"<b>{row['city']}</b><br>Total Processing: ${row['Total_Processing']:,.2f}<br>Transactions: {int(row['Total_Transactions'])}<br>Address: {row['full_address']}",
                axis=1
            ),
            mode='markers',
            marker=dict(
                size=territory_data_plot['size'], # Use calculated size based on processing
                color='#818cf8',
                opacity=0.7,
                line=dict(width=1, color='rgba(255, 255, 255, 0.5)')
            ),
            name='Processing by Location', # Updated name
            hoverinfo='text'
        ))

    # Update the geo layout properties
    fig.update_layout(
        title={
            'text': 'Processing Amount by Location (Selected Period)', # Updated title
            'font': {'family': 'Roboto, sans-serif', 'size': 18, 'color': '#1e293b'},
            'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        showlegend=False,
        geo=dict(
            scope='usa', projection_type='albers usa', showland=True, landcolor='rgb(250, 250, 250)', countrycolor='rgb(204, 204, 204)', showlakes=True, lakecolor='rgb(255, 255, 255)', showsubunits=True, subunitcolor='rgb(230, 230, 230)', bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=40, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_profit_by_location_map(data, start_date, end_date): # Added date parameters
    """Create a map showing profit by location (City) and total transactions for the selected period"""
    # Filter transactions by date first
    filtered_transactions = data['transactions'][
        (data['transactions']['TRAN_DT'] >= start_date) &
        (data['transactions']['TRAN_DT'] <= end_date)
    ].copy()

    # If no transactions in the period, return an empty map
    if filtered_transactions.empty:
        # st.info("No transaction data in the selected period.") # Optional info message
        fig = go.Figure() # Start with base map structure even if empty
        fig.add_trace(go.Choropleth(
            locationmode='USA-states',
            locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                       'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                       'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                       'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                       'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
            z=[0]*50,
            colorscale=[[0, 'rgba(240, 240, 240, 0.8)'], [1, 'rgba(240, 240, 240, 0.8)']],
            showscale=False,
            marker_line_color='white',
            marker_line_width=0.5
        ))
        fig.update_layout( # Apply basic layout
            title={
                'text': 'Estimated Profit by Location',
                'font': {'family': 'Roboto, sans-serif', 'size': 18, 'color': '#1e293b'}, # Adjusted size
                'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
            },
            showlegend=False,
            geo=dict(scope='usa', projection_type='albers usa', showland=True, landcolor='rgb(250, 250, 250)', countrycolor='rgb(204, 204, 204)', bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=40, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig # Return the empty-looking map

    # Aggregate filtered transactions by City
    territory_data = filtered_transactions.groupby('CITY_NM').agg(
        Total_Processing=('TRAN_AM', 'sum'),
        Total_Transactions=('TransactionVolume', 'sum'),
        latitude=('latitude', 'first'),
        longitude=('longitude', 'first'),
        full_address=('preprocessed_address', 'first')
    ).reset_index()

    # Rename city column
    territory_data = territory_data.rename(columns={'CITY_NM': 'city'})

    # Data Cleaning and Preparation (similar to load_data)
    required_map_cols = ['city', 'Total_Processing', 'Total_Transactions', 'latitude', 'longitude', 'full_address']
    for col in required_map_cols:
        if col not in territory_data.columns:
            territory_data[col] = np.nan

    territory_data['city'] = territory_data['city'].astype(str).fillna('Unknown')
    territory_data['full_address'] = territory_data['full_address'].astype(str).fillna('Address Unavailable')
    territory_data['latitude'] = pd.to_numeric(territory_data['latitude'], errors='coerce') # Keep as NaN initially
    territory_data['longitude'] = pd.to_numeric(territory_data['longitude'], errors='coerce') # Keep as NaN initially
    territory_data['Total_Processing'] = pd.to_numeric(territory_data['Total_Processing'], errors='coerce').fillna(0)
    territory_data['Total_Transactions'] = pd.to_numeric(territory_data['Total_Transactions'], errors='coerce').fillna(0)

    # Calculate estimated profit
    territory_data['EstimatedProfit'] = territory_data['Total_Processing'] * 0.3

    # Create the figure
    fig = go.Figure()

    # Add base map
    fig.add_trace(go.Choropleth(
        locationmode='USA-states',
        locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                   'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                   'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                   'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                   'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
        z=[0]*50,
        colorscale=[[0, 'rgba(240, 240, 240, 0.8)'], [1, 'rgba(240, 240, 240, 0.8)']],
        showscale=False,
        marker_line_color='white',
        marker_line_width=0.5
    ))

    # Add bubbles for each city
    # Filter out entries with invalid lat/lon AFTER aggregation
    territory_data_plot = territory_data[
        territory_data['latitude'].notna() &
        territory_data['longitude'].notna() &
        (territory_data['latitude'] != 0) &
        (territory_data['longitude'] != 0)
    ].copy()

    if not territory_data_plot.empty:
        max_profit = territory_data_plot['EstimatedProfit'].max() if territory_data_plot['EstimatedProfit'].max() > 0 else 1
        min_size = 15
        max_size = 50
        # Use EstimatedProfit for bubble size
        territory_data_plot['size'] = min_size + (territory_data_plot['EstimatedProfit'] / max_profit) * (max_size - min_size)

        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=territory_data_plot['longitude'],
            lat=territory_data_plot['latitude'],
            # Use columns from territory_data_plot
            text=territory_data_plot.apply(
                lambda row: f"<b>{row['city']}</b><br>Est. Profit: ${row['EstimatedProfit']:,.2f}<br>Transactions: {int(row['Total_Transactions'])}<br>Address: {row['full_address']}",
                axis=1
            ),
            mode='markers',
            marker=dict(
                size=territory_data_plot['size'], # Use calculated size
                color='#818cf8', # Bubble color
                opacity=0.7,
                line=dict(width=1, color='rgba(255, 255, 255, 0.5)')
            ),
            name='Profit by Location',
            hoverinfo='text'
        ))

    # Update the geo layout properties
    fig.update_layout(
        title={
            'text': 'Estimated Profit by Location',
            'font': {
                'family': 'Roboto, sans-serif',
                'size': 18, # Adjusted size
                'color': '#1e293b'
            },
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(250, 250, 250)', # Light gray land
            countrycolor='rgb(204, 204, 204)', # Gray country borders
            showlakes=True, # Show lakes
            lakecolor='rgb(255, 255, 255)', # White lakes
            showsubunits=True, # Show state lines
            subunitcolor='rgb(230, 230, 230)', # Light gray state lines
            bgcolor='rgba(0,0,0,0)' # Transparent background for the geo plot area
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=450,
        paper_bgcolor='rgba(0,0,0,0)', # Transparent background for the whole chart area
        plot_bgcolor='rgba(0,0,0,0)' # Transparent background for the plot area itself
    )
    return fig

def create_processing_by_account_chart(data, start_date, end_date):
    """Create a bar chart showing the distribution of processing amount by account name for the selected period"""
    # Filter transactions first
    transactions = data['transactions'][
        (data['transactions']['TRAN_DT'] >= start_date) &
        (data['transactions']['TRAN_DT'] <= end_date)
    ].copy()

    # If no transactions, return empty figure
    if transactions.empty:
        fig = go.Figure()
        fig.update_layout(title='Top 10 Accounts by Processing Amount')
        return fig

    # Ensure needed columns exist and fill NAs
    required_cols = ['LCTN_ID', 'CHILD_LCTN_DBA_NM', 'GRANDPARENT_CORP_DBA_NM', 'REP NAME', 'TRAN_AM', 'TransactionVolume']
    for col in required_cols:
        if col not in transactions.columns:
            transactions[col] = np.nan # Add missing cols

    transactions['CHILD_LCTN_DBA_NM'] = transactions['CHILD_LCTN_DBA_NM'].fillna('Unknown Account')
    transactions['GRANDPARENT_CORP_DBA_NM'] = transactions['GRANDPARENT_CORP_DBA_NM'].fillna('N/A')
    transactions['REP NAME'] = transactions['REP NAME'].fillna('Unknown Rep')
    transactions['TRAN_AM'] = transactions['TRAN_AM'].fillna(0)

    # Aggregate total processing amount by LCTN_ID, including hierarchy and rep name
    account_totals = transactions.groupby(
        ['LCTN_ID', 'CHILD_LCTN_DBA_NM', 'GRANDPARENT_CORP_DBA_NM', 'REP NAME']
    ).agg(
        ProcessingAmount=('TRAN_AM', 'sum')
    ).reset_index()

    # REMOVED: Merges with accounts and sales_reps tables as names are now grouped directly

    # Handle cases where grouping might result in empty dataframe (though unlikely if transactions wasn't empty)
    if account_totals.empty:
        fig = go.Figure()
        fig.update_layout(title='Top 10 Accounts by Processing Amount')
        return fig

    # Sort by processing amount (descending)
    account_totals = account_totals.sort_values('ProcessingAmount', ascending=False)

    # Take top 10 accounts for better visibility
    top_accounts = account_totals.head(10)

    # Calculate percentage of total within the filtered period
    total_processing_period = account_totals['ProcessingAmount'].sum()
    top_accounts['Percentage'] = (top_accounts['ProcessingAmount'] / total_processing_period * 100) if total_processing_period > 0 else 0

    # Rename columns for clarity in chart text/hover
    top_accounts = top_accounts.rename(columns={
        'CHILD_LCTN_DBA_NM': 'AccountName',
        'GRANDPARENT_CORP_DBA_NM': 'GrandparentName',
        'REP NAME': 'RepName'
    })

    # Create the bar chart
    fig = go.Figure()

    # Generate a colorful palette
    colors = px.colors.qualitative.Vivid # Using a different Plotly Express palette

    # Add the bar trace
    fig.add_trace(go.Bar(
        x=top_accounts['AccountName'], # Use Child Name for x-axis
        y=top_accounts['ProcessingAmount'],
        # Text on bars: Amount, Percentage, Rep Name (matching image)
        text=[f"${amt:,.2f}<br>({pct:.1f}%)<br>{rep}" for amt, pct, rep in
              zip(top_accounts['ProcessingAmount'],
                  top_accounts['Percentage'],
                  top_accounts['RepName'])],
        textposition='auto', # Changed to auto; might need adjustment based on bar height
        textfont=dict(size=10), # Smaller font for text on bars
        marker_color=colors[:len(top_accounts)], # Use the new color palette
        hoverinfo='text',
        # Hover Text: Include Grandparent Name
        hovertext=[f"Account: {name}<br>Grandparent: {gp}<br>Amount: ${amt:,.2f}<br>Percentage: {pct:.1f}%<br>Rep: {rep}"
                   for name, gp, amt, pct, rep in
                   zip(top_accounts['AccountName'],
                       top_accounts['GrandparentName'],
                       top_accounts['ProcessingAmount'],
                       top_accounts['Percentage'],
                       top_accounts['RepName'])]
    ))

    # Update layout
    fig.update_layout(
        title={
            'text': 'Top 10 Accounts by Processing Amount',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'color': '#1e293b'} # Consistent font
        },
        yaxis_title="Processing Amount ($)",
        xaxis_title="Account Name",
        xaxis_tickangle=-45,
        height=500,
        margin=dict(l=50, r=20, t=80, b=120), # Adjusted margins slightly
        plot_bgcolor='white',
        bargap=0.2 # Add some gap between bars
    )

    # Add value formatting to y-axis
    fig.update_yaxes(
        tickprefix="$",
        separatethousands=True,
        gridcolor='rgba(0,0,0,0.05)' # Add light gridlines
    )
    fig.update_xaxes(
        gridcolor='rgba(0,0,0,0.05)' # Add light gridlines
    )


    return fig

def create_management_transaction_table(data, start_date, end_date):
    """Create a detailed transaction table for management view for the selected period, showing Grandparent as Account Name"""
    # Filter transactions first
    transactions = data['transactions'][
        (data['transactions']['TRAN_DT'] >= start_date) &
        (data['transactions']['TRAN_DT'] <= end_date)
    ].copy() # Has LCTN_ID and hierarchy columns

    # If no transactions in the period, return an empty DataFrame with expected columns
    if transactions.empty:
        return pd.DataFrame(columns=[
            'RepName', 'AccountName', # Only Grandparent Name displayed as AccountName
            'Sum of ProcessingAmount', 'Count of TransactionVolume'
        ])

    # Ensure the necessary columns exist and handle potential missing values
    required_cols = ['REP NAME', 'GRANDPARENT_CORP_DBA_NM', 'TRAN_AM', 'TransactionVolume']
    for col in required_cols:
        if col not in transactions.columns:
             # Use appropriate fill for missing columns
             fill_value = 'N/A' if col == 'GRANDPARENT_CORP_DBA_NM' else ('Unknown Rep' if col == 'REP NAME' else 0)
             transactions[col] = fill_value
        else:
             # Fill missing values specifically for these columns
             if col == 'REP NAME':
                 transactions[col] = transactions[col].fillna('Unknown Rep')
             elif col == 'GRANDPARENT_CORP_DBA_NM':
                 transactions[col] = transactions[col].fillna('N/A')
             elif col == 'TRAN_AM' or col == 'TransactionVolume':
                 transactions[col] = transactions[col].fillna(0)


    # Group by RepName and the GRANDPARENT_CORP_DBA_NM (Grandparent Name)
    grouped = transactions.groupby(
        ['REP NAME', 'GRANDPARENT_CORP_DBA_NM'] # Group by Rep and Grandparent only
    ).agg(
        TRAN_AM=('TRAN_AM', 'sum'),           # Use named aggregation
        TransactionVolume=('TransactionVolume', 'sum')
    ).reset_index()

    # Rename columns for display
    grouped = grouped.rename(columns={
        'REP NAME': 'RepName',
        'GRANDPARENT_CORP_DBA_NM': 'AccountName', # Rename Grandparent to AccountName
        # Removed Parent/Child renames
        'TRAN_AM': 'Sum of ProcessingAmount',
        'TransactionVolume': 'Count of TransactionVolume'
    })

    # Format currency columns
    grouped['Sum of ProcessingAmount'] = grouped['Sum of ProcessingAmount'].apply(
        lambda x: f"${x:,.2f}"
    )

    # Sort by rep name and processing amount
    grouped = grouped.sort_values(['RepName', 'Sum of ProcessingAmount'], ascending=[True, False])

    # Select and order columns for display (RepName, AccountName, Amount, Volume)
    return grouped[[
        'RepName', 'AccountName',
        'Sum of ProcessingAmount', 'Count of TransactionVolume'
    ]]

def calculate_management_metrics(data, start_date, end_date):
    """Calculate overall metrics for management dashboard"""
    # Filter transactions using TRAN_DT
    filtered_transactions = data['transactions'][
        (data['transactions']['TRAN_DT'] >= start_date) & # Use TRAN_DT instead of TransactionDate
        (data['transactions']['TRAN_DT'] <= end_date)
    ].copy() # Add .copy()

    # Calculate totals using TRAN_AM and TransactionVolume
    total_processing = filtered_transactions['TRAN_AM'].sum() # Use TRAN_AM
    total_volume = filtered_transactions['TransactionVolume'].sum() # Use TransactionVolume

    # Get total YTD goal from all reps (RepID is name)
    total_ytd_goal = data['sales_targets']['BonusThreshold'].sum()

    # Calculate overall completion percentage - multiply by 100 to show as percentage
    completion_percentage = round((total_processing / total_ytd_goal) * 100, 2) if total_ytd_goal > 0 else 0

    # Count reps eligible for bonus based on actual performance vs targets
    eligible_count = 0
    if 'sales_reps' in data and not data['sales_reps'].empty:
        for rep_id in data['sales_reps']['RepID'].unique():
             # Use calculate_rep_metrics which is already updated
             rep_metrics = calculate_rep_metrics(data, rep_id, start_date, end_date)
             if rep_metrics['bonus_eligibility']:
                 eligible_count += 1

    return {
        'total_processing': total_processing,
        'total_volume': total_volume,
        'total_ytd_goal': total_ytd_goal,
        'completion_percentage': completion_percentage,
        'bonus_eligible_count': eligible_count # Use calculated count based on updated rep metrics
    }

def show_login_page():
    # Hide all Streamlit elements
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {padding-top: 0px;}
            .css-18e3th9 {padding-top: 0px;}
            .css-1d391kg {padding-top: 0px;}
            div[data-testid="stAppViewBlockContainer"] {background-color: #f5f7fa; padding-top: 0;}
            div[data-testid="stVerticalBlock"] {gap: 0;}
            
            /* Remove default Streamlit styling */
            .stTextInput > div > div > input {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px 16px;
            }
            
            .stButton > button {
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: 600;
                width: 100%;
                border: none;
            }
            
            /* Style for radio buttons to look like tabs */
            .stRadio > div {
                display: flex;
                flex-direction: row;
                gap: 10px;
            }
            
            .stRadio > div > div {
                flex: 1;
            }
            
            .stRadio > div > div > label {
                display: block;
                background-color: #f3f4f6;
                padding: 10px 15px;
                text-align: center;
                border-radius: 8px;
                cursor: pointer;
            }
            
            /* Hide the actual radio button */
            .stRadio > div > div > label > div > div:first-child {
                display: none;
            }
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Create columns to center the login form
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Add custom CSS for styling
        st.markdown("""
        <style>
        .login-header {
            text-align: center;
            margin-bottom: 10px;
            color: #1f2937;
            font-weight: 700;
            font-size: 24px;
        }
        
        .login-subheader {
            text-align: center;
            margin-bottom: 30px;
            color: #6b7280;
            font-size: 16px;
        }
        
        .gradient-text {
            background: linear-gradient(90deg, #1E88E5, #0D47A1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        
        .form-label {
            font-weight: 500;
            color: #4b5563;
            margin-bottom: 8px;
            display: block;
        }
        
        .footer-text {
            text-align: center;
            margin-top: 30px;
            color: #6b7280;
            font-size: 12px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Center the logo
        _, logo_col, _ = st.columns([1, 1, 1])
        with logo_col:
            # Changed from fractal_logo.png to Sky_Systemz_Logo.jpg
            st.image('Sky_Systemz_Logo.jpg', width=300, use_container_width=False)
        
        # Header and subheader
        st.markdown('<h1 class="login-header">Welcome to <span class="gradient-text">Sky Systemz</span></h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subheader">The most efficient payment system</p>', unsafe_allow_html=True)
        
        # User type selector
        st.markdown('<label class="form-label">Select your role:</label>', unsafe_allow_html=True)
        user_type = st.radio(
            "",
            ["Sales Representative", "Management"],
            horizontal=True,
            key="user_type_selector",
            label_visibility="collapsed"
        )
        
        # Username and password inputs
        st.markdown('<label class="form-label">Username</label>', unsafe_allow_html=True)
        username = st.text_input("", placeholder="Enter your username", label_visibility="collapsed")
        
        st.markdown('<label class="form-label">Password</label>', unsafe_allow_html=True)
        password = st.text_input("", placeholder="Enter your password", type="password", label_visibility="collapsed")
        
        # Login button
        login_button = st.button("Sign In", use_container_width=True)
        

        # Load users from YAML file
        yaml_data = yaml.safe_load(open('users.yaml'))
        usernames = [user['username'] for user in yaml_data.get('users', [])]
        passwords = [user['password'] for user in yaml_data.get('users', [])]
        roles = [user['role'] for user in yaml_data.get('users', [])]
        sale_rep_name = [user['name'] for user in yaml_data.get('users', [])]


        if login_button:
            if username in usernames and passwords[usernames.index(username)] == password:
                user_role = roles[usernames.index(username)]
                if user_role == user_type:
                    st.session_state.authenticated = True
                    st.session_state.user_role =     user_role
                    st.session_state.sale_rep_name = sale_rep_name[usernames.index(username)]
                    st.rerun()
                else:
                    st.error("Invalid Role Type. Please select the correct role for your account.")
            else:
                st.error("Invalid Username or Password")
        
        # Footer
        st.markdown('<p class="footer-text">© 2025 Sky Systemz. All rights reserved.</p>', unsafe_allow_html=True)

def show_dashboard():
    if st.session_state.authenticated:
        data = load_data()
        #filter the data to only include the sales rep's account
        if data is None:
            return

    # Create a clean, modern header with larger logo
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1E88E5, #2196F3); 
                color: white; 
                padding: 20px 30px; 
                margin-bottom: 30px; 
                display: flex; 
                justify-content: space-between; 
                align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 600;">Sales Rep Dashboard</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 16px;">
                Sales Representative View
            </p>
        </div>
        <img src="data:image/png;base64,{}" style="height: 60px; margin-right: 10px;">
    </div>
    """.format(
        base64.b64encode(open('Sky_Systemz_Logo.jpg', 'rb').read()).decode()
    ), unsafe_allow_html=True)

    st.sidebar.header("Filters")
    
    # Date filters - Use min date from data but allow selection up to current day
    min_date = data['transactions']['TRAN_DT'].min().date()
    today = datetime.now().date()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=today
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=today,  # Default to today
            min_value=min_date,
            max_value=today
        )
    
    # Rep selection section
    rep_options = data['sales_reps'][['RepID', 'RepName']].copy()
    rep_options['Display'] = rep_options['RepName'] + " (ID: " + rep_options['RepID'].astype(str) + ")"
    
    # Rep Selection - Now always available
    st.sidebar.markdown("---")
    st.sidebar.subheader("Rep Selection")
    # Determine default index - if management, first rep; if rep, try to find them (or default to 0)
    default_rep_index = 0
    # Note: Without proper login identifying the *specific* rep, 
    # we'll still default to the first rep for the initial view in the rep role.
    # A better approach would involve storing the logged-in rep's ID in session_state.

    if st.session_state.get('user_role') == "Sales Representative":
        options = st.session_state.sale_rep_name
    else:
        options = rep_options['RepID'].tolist()
    
    rep_id = st.sidebar.selectbox(
        "Select Sales Rep",
        options=options,
        format_func=lambda x: rep_options[rep_options['RepID'] == x]['Display'].iloc[0] if not rep_options[rep_options['RepID'] == x].empty else f"{x} (No data found)",
        index=default_rep_index # Default to the first rep initially
    )
    
    # Check if rep exists in the data
    rep_exists = not rep_options[rep_options['RepID'] == rep_id].empty
    if not rep_exists:
        st.warning(f"No data found for sales representative: {rep_id}")
        # Exit the function to avoid showing any data
        return
    
    # Tabs depend on the role
    if st.session_state.get('user_role') == "Management":
        st.sidebar.markdown("*Note: Rep selection also filters the Rep Dashboard and Compensation Model tabs.*")
        tabs = ["Management Overview", "Rep Dashboard", "Compensation Model"]
    else: # Sales Representative Role
        st.sidebar.markdown("Select your name to view your specific data.")
        tabs = ["Dashboard", "Compensation Model"]
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Using tabs to separate Dashboard views
    selected_tab = st.tabs(tabs)
    
    # Management Overview Tab (only visible to management users)
    if st.session_state.get('user_role') == "Management" and selected_tab[0]:
        with selected_tab[0]:
            # Calculate management metrics
            mgmt_metrics = calculate_management_metrics(data, start_date, end_date)
            
            # Format values
            formatted_volume = str(int(mgmt_metrics["total_volume"]))
            formatted_amount = f"${mgmt_metrics['total_processing']/1000:.2f}K"
            formatted_goal = f"${mgmt_metrics['total_ytd_goal']/1000:.2f}K"
            formatted_completion = f"{mgmt_metrics['completion_percentage']:.1f}%"
            formatted_bonus_count = str(mgmt_metrics["bonus_eligible_count"])

            # Use st.columns for reliable display
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.markdown("<div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>TOTAL VOLUME TRANSACTIONS</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #4338ca; font-size: 28px; font-weight: 700;'>{formatted_volume}</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>TOTAL PROCESSING AMOUNT</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #3b82f6; font-size: 28px; font-weight: 700;'>{formatted_amount}</div>", unsafe_allow_html=True)

            with col3:
                st.markdown("<div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>TOTAL YTD GOAL</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #4338ca; font-size: 28px; font-weight: 700;'>{formatted_goal}</div>", unsafe_allow_html=True)

            with col4:
                st.markdown("<div style='background-color: #fdf2f8; padding: 10px; border-radius: 5px;'><div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>TOTAL COMPLETION %</div><div style='color: #4338ca; font-size: 28px; font-weight: 700;'>{}</div></div>".format(formatted_completion), unsafe_allow_html=True)

            with col5:
                st.markdown("<div style='background-color: #f5f3ff; padding: 10px; border-radius: 5px;'><div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>BONUS ELIGIBILITY COUNT</div><div style='color: #4338ca; font-size: 28px; font-weight: 700;'>{}</div></div>".format(formatted_bonus_count), unsafe_allow_html=True)
            
            # Add Activity Summary Table (NEW) but keep all other visualizations
            st.markdown("## Team Activity Performance Summary")
            
            # Get the summary tables, passing the date filters
            summary_df, metrics_df, top_performers = create_activity_summary_table(data, start_date, end_date)
            
            # Format summary table
            formatted_summary = summary_df.copy()
            # Format numeric columns
            for col in formatted_summary.columns:
                if col == 'Metric':
                    continue
                if col == 'Standard Deviation' or col == 'Average':
                    for idx, metric in enumerate(formatted_summary['Metric']):
                        if metric == 'Goal Achievement (%)':
                            formatted_summary.loc[idx, col] = f"{formatted_summary.loc[idx, col]:.1f}%"
                        else:
                            formatted_summary.loc[idx, col] = f"{formatted_summary.loc[idx, col]:.1f}"
                elif col == 'Total':
                    # Don't format the 'None' value for Goal Achievement
                    for idx, metric in enumerate(formatted_summary['Metric']):
                        if metric != 'Goal Achievement (%)' and formatted_summary.loc[idx, col] is not None:
                            formatted_summary.loc[idx, col] = f"{formatted_summary.loc[idx, col]:.0f}"
            
            # Display the summary table
            st.dataframe(formatted_summary, use_container_width=True)
            
            # # Display top performers - Now show top 5 based on transaction amount
            # st.markdown("### Top Performing Sales Representatives")
            
            # # Get transaction data for all reps
            # transactions_data = data.get('transactions')
            # if transactions_data is not None and not transactions_data.empty:
            #     # Ensure TRAN_DT is datetime
            #     transactions_data['TRAN_DT'] = pd.to_datetime(transactions_data['TRAN_DT'], errors='coerce')
                
            #     # Filter by date range
            #     filtered_transactions = transactions_data[
            #         (transactions_data['TRAN_DT'] >= start_date) &
            #         (transactions_data['TRAN_DT'] <= end_date)
            #     ]
                
            #     # Calculate total amount for each rep
            #     rep_amounts = filtered_transactions.groupby('REP NAME')['TRAN_AM'].sum().reset_index()
            #     rep_amounts = rep_amounts.rename(columns={'REP NAME': 'RepName', 'TRAN_AM': 'Total Amount'})
                
            #     # Get top 5 reps by transaction amount
            #     top_reps = rep_amounts.sort_values('Total Amount', ascending=False).head(5)
                
            #     # Format as currency
            #     top_reps['Total Amount'] = top_reps['Total Amount'].apply(lambda x: f"${x:,.2f}")
            #     # Rename column for display
            #     top_formatted = top_reps.rename(columns={'Total Amount': 'Total Processed Amount'})
            # else:
            #     # If no transaction data, create an empty dataframe with appropriate columns
            #     top_formatted = pd.DataFrame(columns=['RepName', 'Total Processed Amount'])
            #     top_formatted['Total Processed Amount'] = '$0.00'  # Default display
            
            # st.dataframe(top_formatted, use_container_width=True)
            
            # RESTORE: Revenue vs Profit Comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                # Pass dates to the function
                revenue_chart = create_revenue_comparison(data, start_date, end_date)
                st.plotly_chart(revenue_chart, use_container_width=True, key="mgmt_revenue_comp")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                # Call the renamed function, passing dates
                processing_location_map = create_processing_by_location_map(data, start_date, end_date) # Pass dates
                st.plotly_chart(processing_location_map, use_container_width=True, key="mgmt_processing_location_map")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # RESTORE: Sales Team Bonus Attainment
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Sales Team Bonus Attainment")
            # NOTE: This chart likely represents YTD/overall bonus attainment, not filtered by date.
            bonus_chart = create_simple_bonus_chart(data, rep_id)
            st.plotly_chart(bonus_chart, use_container_width=True, key="mgmt_bonus_chart")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # RESTORE: Processing by Account chart (as bar chart now)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Pass dates to the function
            processing_by_account_chart = create_processing_by_account_chart(data, start_date, end_date)
            st.plotly_chart(processing_by_account_chart, use_container_width=True, key="mgmt_account_chart")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # RESTORE: Transaction table
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.subheader("Transaction Details by Sales Representative and Account")
            # Pass dates to the function
            transaction_table = create_management_transaction_table(data, start_date, end_date)
            st.dataframe(transaction_table, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Rep Dashboard Tab
    rep_tab_index = 0 if st.session_state.get('user_role') != "Management" else 1
    if selected_tab[rep_tab_index]:
        with selected_tab[rep_tab_index]:
            # For management view, we need to ensure rep_id is selected
            if st.session_state.get('user_role') == "Management" and not rep_id:
                st.warning("Please select a Sales Rep from the sidebar to view their dashboard.")
                return
            
            metrics = calculate_rep_metrics(data, rep_id, start_date, end_date)
            
            # Format metric values - keep it simple
            vol_value = str(int(metrics["total_volume"]))
            amount_value = f"${metrics['total_processed']/1000:.2f}K" 
            goal_value = f"${metrics['ytd_goal']/1000:.2f}K"
            completion_value = f"{metrics['completion_percentage']:.1f}%"
            eligibility_value = "Eligible" if metrics["bonus_eligibility"] else "Not Eligible"

            # Use st.columns instead of HTML for more reliable display
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.markdown("<div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>TOTAL VOLUME TRANSACTIONS</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #4338ca; font-size: 28px; font-weight: 700;'>{vol_value}</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>TOTAL OF PROCESSED AMOUNTS</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #3b82f6; font-size: 28px; font-weight: 700;'>{amount_value}</div>", unsafe_allow_html=True)

            with col3:
                st.markdown("<div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>YTD GOAL</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: #4338ca; font-size: 28px; font-weight: 700;'>{goal_value}</div>", unsafe_allow_html=True)

            with col4:
                st.markdown("<div style='background-color: #fdf2f8; padding: 10px; border-radius: 5px;'><div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>TOTAL COMPLETION %</div><div style='color: #4338ca; font-size: 28px; font-weight: 700;'>{}</div></div>".format(completion_value), unsafe_allow_html=True)

            with col5:
                st.markdown("<div style='background-color: #f5f3ff; padding: 10px; border-radius: 5px;'><div style='color: #6b7280; font-size: 12px; text-transform: uppercase;'>BONUS ELIGIBILITY</div><div style='color: #4338ca; font-size: 28px; font-weight: 700;'>{}</div></div>".format(eligibility_value), unsafe_allow_html=True)
            
            # Rest of the dashboard content
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Territory Performance")
            # Pass dates to the function
            map_chart = create_map_visualization(data, rep_id, start_date, end_date) # Pass dates
            st.plotly_chart(map_chart, use_container_width=True, key="rep_map_chart")  # Added unique key
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Continue with other charts (with unique keys)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Remove column division - use full width
            st.subheader("Processing Amount Over Time")
            time_series_chart = create_time_series_chart(data, rep_id, start_date, end_date)
            st.plotly_chart(time_series_chart, use_container_width=True, key="rep_time_series")  # Added unique key
            # Remove the Transaction Volume chart entirely
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.subheader("Transaction Details")
            
            # Get the transaction table data first
            transaction_table = create_transaction_table(data, rep_id, start_date, end_date)
            
            # Add AccountName filter
            if not transaction_table.empty:
                # Get unique AccountNames from the transaction table
                account_names = sorted(transaction_table['AccountName'].unique().tolist())
                
                # Add an "All Accounts" option at the beginning
                account_filter_options = ["All Accounts"] + account_names
                
                # Create the filter dropdown
                selected_account = st.selectbox(
                    "Filter by Account:", 
                    account_filter_options,
                    key="account_filter"
                )
                
                # Apply the filter if a specific account is selected
                if selected_account != "All Accounts":
                    transaction_table = transaction_table[transaction_table['AccountName'] == selected_account]
                
                # Sort the table by Year, Quarter, and Month in descending order (newest first)
                if 'Year' in transaction_table.columns and 'Quarter' in transaction_table.columns and 'Month' in transaction_table.columns:
                    # Convert Month names to numbers for proper sorting
                    month_order = {
                        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                    }
                    
                    # Create temporary numeric month column for sorting
                    if transaction_table['Month'].dtype == 'object':  # If Month is stored as text
                        transaction_table['MonthNum'] = transaction_table['Month'].map(month_order)
                        transaction_table = transaction_table.sort_values(
                            by=['Year', 'Quarter', 'MonthNum'], 
                            ascending=[True, True, True]
                        )
                        # Remove temporary column
                        transaction_table = transaction_table.drop('MonthNum', axis=1)
                    else:  # If Month is already numeric
                        transaction_table = transaction_table.sort_values(
                            by=['Year', 'Quarter', 'Month'], 
                            ascending=[True, True, True]
                        )
            
            # Display the filtered table
            st.dataframe(transaction_table, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add activity performance chart
            st.markdown("## My Activity & Performance Metrics")
            col1, col2 = st.columns(2)
            
            # Determine if this is a management view
            is_management_view = st.session_state.get('user_role') == "Management"
            
            with col1:
                st.subheader("Discovery & Follow-up Activities")
                discovery_chart = create_activity_performance_chart(
                    data.get('performance_data'), 
                    rep_id=rep_id, 
                    start_date=start_date, # Pass start_date
                    end_date=end_date,     # Pass end_date
                    is_management=is_management_view,
                    chart_type="discovery"
                )
                # Check if chart data exists
                if discovery_chart is not None:
                    st.plotly_chart(discovery_chart, use_container_width=True)
                else:
                    st.info("No discovery/follow-up activity data available for this representative in the selected period.")
            
            with col2:
                st.subheader("Demo & Conversion Activities")
                demo_chart = create_activity_performance_chart(
                    data.get('performance_data'), 
                    rep_id=rep_id, 
                    start_date=start_date, # Pass start_date
                    end_date=end_date,     # Pass end_date
                    is_management=is_management_view,
                    chart_type="demo"
                )
                # Check if chart data exists
                if demo_chart is not None:
                    st.plotly_chart(demo_chart, use_container_width=True)
                else:
                    st.info("No demo/conversion activity data available for this representative in the selected period.")
    
    # Compensation Model Tab
    comp_tab_index = 1 if st.session_state.get('user_role') != "Management" else 2
    if selected_tab[comp_tab_index]:
        with selected_tab[comp_tab_index]:
            # Get rep details
            rep_details = data['sales_reps'][data['sales_reps']['RepID'] == rep_id].iloc[0]
            rep_name = rep_details['RepName']
            
            # Get target info
            target_info = data['sales_targets'][data['sales_targets']['RepID'] == rep_id]
            if not target_info.empty:
                bonus_threshold = target_info.iloc[0]['BonusThreshold']
                bonus_eligibility = target_info.iloc[0]['Bonus_Eligibility']
            else:
                bonus_threshold = 0
                bonus_eligibility = False
            
            # Add the bonus attainment scale at the top of the tab
            st.markdown("### Bonus Attainment")
            # Make sure this function is defined above
            bonus_scale = create_bonus_attainment_scale(data, rep_id)
            st.plotly_chart(bonus_scale, use_container_width=True, key="comp_bonus_scale")
            
            # Display summary cards
            st.subheader(f"Compensation Model: {rep_name}")
            st.markdown(f"**Annual Bonus Threshold:** ${bonus_threshold:,.2f}")
            
            # Generate monthly targets and actuals for visualization
            # Get rep accounts (AccountID comes from the accounts dataframe)
            rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id]['AccountID'].tolist()

            # ---- FIX THIS LINE (around 2293) ----
            # Filter the main transactions dataframe using LCTN_ID
            rep_transactions = data['transactions'][
                data['transactions']['LCTN_ID'].isin(rep_accounts) # Ensure this uses LCTN_ID
            ].copy() # Add .copy()

            # Ensure TRAN_DT is datetime
            rep_transactions['TRAN_DT'] = pd.to_datetime(rep_transactions['TRAN_DT']) # Use TRAN_DT

            # Set up monthly data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            
            # Calculate monthly targets (equal distribution)
            monthly_targets = [bonus_threshold/12 for _ in range(6)]  # Monthly targets
            cumulative_targets = [sum(monthly_targets[:i+1]) for i in range(6)]  # Cumulative
            
            # Calculate actual processing by month
            monthly_actuals = []
            for month in range(1, 7):  # Jan-Jun
                # Ensure TRAN_DT is datetime before accessing .dt
                # This conversion should have happened when rep_transactions was created, but double-check
                if not pd.api.types.is_datetime64_any_dtype(rep_transactions['TRAN_DT']):
                     rep_transactions['TRAN_DT'] = pd.to_datetime(rep_transactions['TRAN_DT'], errors='coerce')

                month_data = rep_transactions[
                    rep_transactions['TRAN_DT'].dt.month == month # Use TRAN_DT
                ]
                monthly_actuals.append(month_data['TRAN_AM'].sum()) # Use TRAN_AM

            # Calculate cumulative actuals
            cumulative_actuals = [sum(monthly_actuals[:i+1]) for i in range(6)]
            
            # Ensure cumulative_actuals has 6 values, padding with last value if needed
            if len(cumulative_actuals) < 6:
                 last_val = cumulative_actuals[-1] if cumulative_actuals else 0
                 cumulative_actuals.extend([last_val] * (6 - len(cumulative_actuals)))

            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("### Performance Summary")
                # Now cumulative_targets and cumulative_actuals are defined
                ytd_completion = (cumulative_actuals[5]/cumulative_targets[5])*100 if cumulative_targets[5] > 0 else 0
                
                metrics_data = [
                    {"label": "YTD Target", "value": f"${cumulative_targets[5]:,.2f}"},
                    {"label": "YTD Actual", "value": f"${cumulative_actuals[5]:,.2f}"},
                    {"label": "YTD Completion", "value": f"{ytd_completion:.1f}%", 
                     "color": "green" if ytd_completion >= 100 else "red"},
                    {"label": "Bonus Eligibility", "value": "Eligible" if bonus_eligibility else "Not Eligible",
                     "color": "green" if bonus_eligibility else "red"}
                ]
                
                for metric in metrics_data:
                    col_label, col_value = st.columns([1, 1])
                    with col_label:
                        st.markdown(f"**{metric['label']}:**")
                    with col_value:
                        if "color" in metric:
                            st.markdown(f"<span style='color: {metric['color']}'>{metric['value']}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(metric['value'])
            
            with col2:
                # Continue with YTD Commission Summary
                # Calculate commissions
                base_commission_rate = 1.5  # 1.5% base
                bonus_commission_rate = 2.5  # 2.5% when hitting targets
                
                monthly_base_commissions = [amount * (base_commission_rate/100) for amount in monthly_actuals]
                monthly_bonus_commissions = []
                
                for i, (actual, target) in enumerate(zip(cumulative_actuals, cumulative_targets)):
                    if actual >= target:
                        # Only apply bonus to the amount exceeding target for the month
                        if i == 0:
                            bonus_amount = actual - target
                        else:
                            # Calculate incremental amount exceeding target
                            prev_excess = max(0, cumulative_actuals[i-1] - cumulative_targets[i-1])
                            current_excess = max(0, actual - target)
                            bonus_amount = current_excess - prev_excess
                        
                        bonus_commission = bonus_amount * (bonus_commission_rate/100)
                    else:
                        bonus_commission = 0
                    
                    monthly_bonus_commissions.append(bonus_commission)
                
                total_commissions = [base + bonus for base, bonus in zip(monthly_base_commissions, monthly_bonus_commissions)]
                
                st.markdown("### YTD Commission Summary")
                commission_data = [
                    {"label": "Base Commission", "value": f"${sum(monthly_base_commissions):,.2f}"},
                    {"label": "Bonus Commission", "value": f"${sum(monthly_bonus_commissions):,.2f}"},
                    {"label": "Total Commission", "value": f"${sum(total_commissions):,.2f}", "highlight": True}
                ]
                
                for metric in commission_data:
                    col_label, col_value = st.columns([1, 1])
                    with col_label:
                        st.markdown(f"**{metric['label']}:**")
                    with col_value:
                        if metric.get("highlight"):
                            st.markdown(f"<span style='color: #4f46e5; font-weight: bold; font-size: 1.1em'>{metric['value']}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(metric['value'])
            
            # REMOVE the Performance & Compensation Over Time section
            # DO NOT include create_rep_progress_compensation_chart here
            
            # Restore the original Performance Trends Charts
            st.markdown("## Performance Trends")
            col1, col2 = st.columns(2)
            
            with col1:
                # Target vs Actual Chart
                fig_target_actual = go.Figure()
                fig_target_actual.add_trace(go.Scatter(
                    x=months,
                    y=monthly_targets,
                    mode='lines+markers',
                    name='Monthly Target',
                    line=dict(color='rgba(239, 68, 68, 0.8)', width=2),
                    marker=dict(size=8)
                ))
                
                fig_target_actual.add_trace(go.Scatter(
                    x=months,
                    y=monthly_actuals,
                    mode='lines+markers',
                    name='Monthly Actual',
                    line=dict(color='rgba(59, 130, 246, 0.9)', width=3),
                    marker=dict(size=10),
                    fill='tozeroy',
                    fillcolor='rgba(59, 130, 246, 0.1)'
                ))
                
                # Calculate monthly completion percentage
                for i, (actual, target) in enumerate(zip(monthly_actuals, monthly_targets)):
                    percentage = (actual / target * 100) if target > 0 else 0
                    fig_target_actual.add_annotation(
                        x=months[i],
                        y=actual,
                        text=f"{percentage:.1f}%",
                        showarrow=False,
                        yshift=10,
                        font=dict(size=10)
                    )
                
                fig_target_actual.update_layout(
                    title="Monthly Target vs Actual",
                    height=300,
                    margin=dict(l=40, r=40, t=40, b=40),
                    legend=dict(orientation="h", y=1.1),
                    yaxis=dict(title="Amount ($)"),
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig_target_actual, use_container_width=True, key="comp_target_actual")
                
            with col2:
                # Commission Rates Chart
                fig_commission = go.Figure()
                
                fig_commission.add_trace(go.Bar(
                    x=months,
                    y=monthly_base_commissions,
                    name='Base Commission',
                    marker_color='rgba(59, 130, 246, 0.7)'
                ))
                
                fig_commission.add_trace(go.Bar(
                    x=months,
                    y=monthly_bonus_commissions,
                    name='Bonus Commission',
                    marker_color='rgba(34, 197, 94, 0.8)'
                ))
                
                # Add total values as text
                for i, (base, bonus) in enumerate(zip(monthly_base_commissions, monthly_bonus_commissions)):
                    total = base + bonus
                    fig_commission.add_annotation(
                        x=months[i],
                        y=total,
                        text=f"${total:.2f}",
                        showarrow=False,
                        yshift=10,
                        font=dict(size=10)
                    )
                
                fig_commission.update_layout(
                    title="Monthly Commission Breakdown",
                    height=300,
                    margin=dict(l=40, r=40, t=40, b=40),
                    legend=dict(orientation="h", y=1.1),
                    yaxis=dict(title="Commission ($)"),
                    barmode='stack',
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig_commission, use_container_width=True, key="comp_rates_chart")
            
            # Add map visualization if needed
            st.markdown("## Territory Performance")
            map_chart = create_map_visualization(data, rep_id, start_date, end_date)
            st.plotly_chart(map_chart, use_container_width=True, key="comp_map_chart")
            
            # Add Monthly Performance Tables
            first_half_df, second_half_df = create_monthly_performance_tables(data, rep_id)
            
            # Format the dataframes for display
            formatted_first_half = first_half_df.copy()
            formatted_second_half = second_half_df.copy()
            
            # Format currency columns
            currency_cols = ['Target', 'Actual', 'Base Commission', 'Bonus Commission', 'Total']
            for df in [formatted_first_half, formatted_second_half]:
                for col in currency_cols:
                    df[col] = df[col].apply(lambda x: f"${x:.2f}")
                
                # Format percentage columns
                df['Completion %'] = df['Completion %'].apply(lambda x: f"{x:.1f}%")
                df['Base Rate'] = df['Base Rate'].apply(lambda x: f"{x:.2f}%")
                df['Bonus Rate'] = df['Bonus Rate'].apply(lambda x: f"{x:.2f}%")
            
            # Display first half table
            st.markdown("## Monthly Performance (First Half)")
            st.markdown("January - June 2024")
            st.dataframe(formatted_first_half, use_container_width=True, hide_index=True)
            
            # Display second half table
            st.markdown("## Monthly Performance (Second Half)")
            st.markdown("July - December 2024")
            st.dataframe(formatted_second_half, use_container_width=True, hide_index=True)
    
    # Add the Rep Details section back to the sidebar
    st.sidebar.markdown("---")

def create_bonus_attainment_scale(data, rep_id):
    """
    Create a simple color-coded scale showing bonus attainment percentages
    with a marker indicating where the sales rep stands.
    """
    # Get rep info
    rep_info = data['sales_reps'][data['sales_reps']['RepID'] == rep_id].iloc[0]
    rep_name = rep_info['RepName']
    
    # Get rep's accounts
    rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id]['AccountID'].tolist()
    
    # Get transactions for this rep using LCTN_ID instead of AccountID
    rep_transactions = data['transactions'][
        data['transactions']['LCTN_ID'].isin(rep_accounts)  # Use LCTN_ID instead of AccountID
    ]
    
    # Get target info
    target_info = data['sales_targets'][data['sales_targets']['RepID'] == rep_id]
    if not target_info.empty:
        target = target_info.iloc[0]['BonusThreshold']
        total_processed = rep_transactions['TRAN_AM'].sum()  # Use TRAN_AM instead of ProcessingAmount
        completion_percentage = (total_processed / target * 100) if target > 0 else 0
    else:
        completion_percentage = 0
    
    # Define segments for the scale - updated with blue theme
    segments = [
        ("", "<30%", 0, 30, "#ef4444"),    # Red
        ("40%", "15%", 30, 40, "#ff8000"),  # Dark Orange
        ("50%", "20%", 40, 50, "#ffbf00"),  # Amber
        ("60%", "25%", 50, 60, "#ffff00"),  # Yellow
        ("70%", "30%", 60, 70, "#E3F2FD"),  # Lightest Blue
        ("80%", "35%", 70, 80, "#BBDEFB"),  # Light Blue
        ("90%", "40%", 80, 90, "#90CAF9"),  # Blue 100
        ("100%", "45%", 90, 100, "#64B5F6"), # Blue 200
        ("110%", "50%", 100, 110, "#42A5F5"), # Blue 300
        ("120%", "55%", 110, 120, "#2196F3"), # Blue 400
        ("130%", "60%", 120, 130, "#1E88E5"), # Blue 500
        ("140%", "65%", 130, 140, "#1976D2"), # Blue 600
        ("150%", "70%", 140, 150, "#1565C0"), # Blue 700
        ("160%", "75%", 150, 160, "#0D47A1"), # Blue 800
        ("170%", "80%", 160, 170, "#0277BD"), # Light Blue 800
        ("180%", "85%", 170, 180, "#01579B"), # Light Blue 900
        ("190%", "90%", 180, 190, "#006064"), # Cyan 900
        ("200%", "95%", 190, 200, "#004D40")  # Teal 900
    ]
    
    # Create the figure with exact sizing to match your image
    fig = go.Figure()
    
    # Add the colored segments
    for top_label, bottom_label, start, end, color in segments:
        fig.add_trace(go.Bar(
            x=[end - start],
            y=[0],
            orientation='h',
            marker=dict(
                color=color,
                line=dict(width=1, color='white')
            ),
            showlegend=False,
            hoverinfo='none',
            base=start,
            text=bottom_label,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="black", size=10)
        ))
        
        # Add top row percentage labels
        fig.add_annotation(
            x=(start + end) / 2,
            y=0.6,
            text=top_label,
            showarrow=False,
            font=dict(size=10)
        )
    
    # Add special markers for key thresholds
    fig.add_shape(
        type="line",
        x0=100, y0=-0.3,
        x1=100, y1=0.3,
        line=dict(color="black", width=2),
    )
    
    # Add 100% label in the divider
    fig.add_annotation(
        x=100,
        y=0,
        text="100%",
        showarrow=False,
        font=dict(size=10, color="white", family="Arial")
    )
    
    # Add CAP text at the end
    fig.add_annotation(
        x=198,
        y=0,
        text="CAP",
        showarrow=False,
        font=dict(size=10, color="red", family="Arial")
    )
    
    # Add rep's position marker
    marker_position = min(200, max(0, completion_percentage))
    
    # Add triangle marker pointing down to show position
    fig.add_trace(go.Scatter(
        x=[marker_position],
        y=[0.3],
        mode='markers+text',
        marker=dict(
            symbol='triangle-down',
            size=15,
            color='black',
        ),
        text=[f"{completion_percentage:.1f}%"],
        textposition='top center',
        textfont=dict(color='black', size=12),
        showlegend=False
    ))
    
    # Update layout to match your image
    fig.update_layout(
        title={
            'text': f"Sales Bonus % Attainment",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=14)
        },
        height=110,
        margin=dict(l=20, r=20, t=40, b=10),
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            range=[-0.5, 0.8],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        barmode='stack',
        hovermode=False
    )
    
    return fig

def create_simple_bonus_chart(data, rep_id):
    """
    Create a horizontal bar chart showing bonus attainment for all sales reps
    """
    # Get all reps data
    all_reps_data = []
    for _, rep in data['sales_reps'].iterrows():
        rep_id_current = rep['RepID'] # This is the REP NAME string
        rep_name = rep['RepName']
        
        # Get transactions using LCTN_ID
        rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id_current]['AccountID'].tolist()
        rep_transactions = data['transactions'][
            data['transactions']['LCTN_ID'].isin(rep_accounts) # Use LCTN_ID instead of AccountID
        ]
        
        # Get target info (RepID is name)
        target_info = data['sales_targets'][data['sales_targets']['RepID'] == rep_id_current]
        if not target_info.empty:
            target = target_info.iloc[0]['BonusThreshold']
            total_processed = rep_transactions['TRAN_AM'].sum() # Use TRAN_AM instead of ProcessingAmount
            completion_percentage = (total_processed / target * 100) if target > 0 else 0
        else:
            target = 0
            total_processed = 0
            completion_percentage = 0
            
        all_reps_data.append({
            'RepID': rep_id_current,
            'RepName': rep_name,
            'Completion': completion_percentage,
            'IsCurrentRep': rep_id_current == rep_id # Compare names
        })
    
    # Sort by completion percentage
    all_reps_data = sorted(all_reps_data, key=lambda x: x['Completion'])
    
    # Create the horizontal bar chart
    fig = go.Figure()
    
    # Add bars for each rep
    for rep_data in all_reps_data:
        # Set color based on whether this is the current rep
        bar_color = '#1E88E5' if rep_data['IsCurrentRep'] else '#94a3b8'
        
        # Set brighter colors for different levels of completion
        if rep_data['Completion'] >= 100:
            bar_color = '#22c55e' if rep_data['IsCurrentRep'] else '#4ade80'  # Green
        elif rep_data['Completion'] >= 50:
            bar_color = '#1E88E5' if rep_data['IsCurrentRep'] else '#42A5F5'  # Blue
        elif rep_data['Completion'] >= 30:
            bar_color = '#f59e0b' if rep_data['IsCurrentRep'] else '#fbbf24'  # Amber
        else:
            bar_color = '#ef4444' if rep_data['IsCurrentRep'] else '#f87171'  # Red
        
        fig.add_trace(
            go.Bar(
                y=[rep_data['RepName']],
                x=[rep_data['Completion']],
                orientation='h',
                marker_color=bar_color,
                text=[f"{rep_data['Completion']:.1f}%"],
                textposition='outside',
                hoverinfo='text',
                hovertext=f"{rep_data['RepName']}: {rep_data['Completion']:.1f}%",
                name=rep_data['RepName']
            )
        )
    
    # Rest of the function remains the same

    # Add a vertical line at 100%
    fig.add_shape(
        type="line",
        x0=100, y0=-0.5,
        x1=100, y1=len(all_reps_data) - 0.5,
        line=dict(color="#f43f5e", width=2, dash="dash")
    )
    
    # Add a vertical line at 30% (bonus eligibility)
    fig.add_shape(
        type="line",
        x0=30, y0=-0.5,
        x1=30, y1=len(all_reps_data) - 0.5,
        line=dict(color="#a1a1aa", width=2, dash="dot")
    )
    
    # Add annotations for target lines
    fig.add_annotation(
        x=100, y=len(all_reps_data) - 0.5,
        text="Target (100%)",
        showarrow=False,
        yshift=10,
        xshift=0,
        font=dict(color="#f43f5e")
    )
    
    fig.add_annotation(
        x=30, y=len(all_reps_data) - 0.5,
        text="Bonus Eligible (30%)",
        showarrow=False,
        yshift=10,
        xshift=0,
        font=dict(color="#a1a1aa")
    )
    
    # Update layout
    fig.update_layout(
        title="Bonus Attainment by Sales Representative (%)",
        xaxis_title="Completion Percentage",
        yaxis_title="Sales Representative",
        height=max(350, 50 * len(all_reps_data)),  # Dynamic height based on number of reps
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(range=[0, max(150, max(rep['Completion'] for rep in all_reps_data) * 1.1)]),
        yaxis=dict(categoryorder='array', categoryarray=[rep['RepName'] for rep in all_reps_data]),
        showlegend=False,
        plot_bgcolor='white'
    )
    
    return fig

def create_activity_performance_chart(performance_data, rep_id=None, start_date=None, end_date=None, is_management=False, chart_type="discovery"):
    """
    Create activity performance chart using actual performance data, 
    filtered by date range and grouped by Year-Month.
    chart_type: "discovery" or "demo"
    """
    
    # Define metrics based on chart type
    # ... (metric definitions remain the same) ...
    if chart_type == "discovery":
        metrics_to_plot = [
            "Discovery Call", 
            "F/U Call", 
            "Email",          # Added Email
            "DM Added", 
            "Discovery Visit", # Added Discovery Visit
            "F/U Visit"
        ]
        title = "Discovery & Follow-up Activities (Actuals)"
        metric_rename_map = {
            "Discovery Call": "Disc. Call",
            "F/U Call": "F/U Call",
            "Email": "Email",
            "DM Added": "DM Added",
            "Discovery Visit": "Disc. Visit",
            "F/U Visit": "F/U Visit"
        }
    else:  # demo
        metrics_to_plot = [
            "Demo Scheduled", 
            "Demo Completed",
            "Registration"
            # "Closed Won" is not in the provided data structure
        ]
        title = "Demo & Conversion Activities (Actuals)"
        metric_rename_map = {
            "Demo Scheduled": "Demo Sched.",
            "Demo Completed": "Demo Comp.",
            "Registration": "Reg."
        }
    
    # Basic data validation
    if performance_data is None or performance_data.empty:
        # st.warning("No performance data available to plot.") # Keep warnings minimal
        return None
        
    required_cols = metrics_to_plot + ['Sales Rep', 'Date', 'Month', 'Year'] # Ensure 'Date' is required
    missing_cols = [col for col in required_cols if col not in performance_data.columns]
    if missing_cols:
        st.warning(f"Performance data is missing required columns: {', '.join(missing_cols)}. Cannot create activity chart.")
        return None

    # --- Data Filtering ---
    # ALWAYS filter by the selected rep_id if provided
    if rep_id:
        # Check if rep_id exists in the data
        if rep_id not in performance_data['Sales Rep'].unique():
             st.info(f"No performance data found for Rep: {rep_id}")
             return None
        filtered_data = performance_data[performance_data['Sales Rep'] == rep_id].copy()
    else:
        # This case should ideally not happen if a rep is always selected,
        # but handle it just in case. Could show all data or a message.
        st.warning("No Sales Rep selected for activity charts.")
        # Option 1: Show all data (if desired for some default state)
        # filtered_data = performance_data.copy()
        # Option 2: Return None (no chart)
        return None

    if filtered_data.empty:
         st.info(f"No performance data found for Rep: {rep_id}")
         return None
             
    # Filter by Date Range (use .loc to avoid SettingWithCopyWarning)
    if start_date and end_date:
        # Ensure start_date and end_date are Timestamps if not already
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Ensure 'Date' column in filtered_data is datetime
        filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], errors='coerce')
        filtered_data = filtered_data.dropna(subset=['Date']) # Drop if Date conversion failed
        
        filtered_data = filtered_data.loc[
            (filtered_data['Date'] >= start_date) & (filtered_data['Date'] <= end_date)
        ].copy()
        
        if filtered_data.empty:
            st.info(f"No activity recorded for Rep: {rep_id} between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}.")
            return None
            
    # --- Aggregation --- 
    # Group data by Year and numeric Month, then sum metrics
    # Ensure 'Month' and 'Year' are numeric for correct grouping/sorting
    filtered_data['Month'] = pd.to_numeric(filtered_data['Month'], errors='coerce')
    filtered_data['Year'] = pd.to_numeric(filtered_data['Year'], errors='coerce')
    filtered_data = filtered_data.dropna(subset=['Month', 'Year']) # Drop rows where conversion failed
    
    # Convert month/year to integer after ensuring they are numeric and not NaN
    filtered_data['Month'] = filtered_data['Month'].astype(int)
    filtered_data['Year'] = filtered_data['Year'].astype(int)

    monthly_agg = filtered_data.groupby(['Year', 'Month'])[metrics_to_plot].sum().reset_index()

    # Sort numerically before creating labels
    monthly_agg = monthly_agg.sort_values(by=['Year', 'Month'])

    # Create proper 'Year-Month-Label' for x-axis using month abbreviations
    try:
        # Get month abbreviation (e.g., 'Jan', 'Feb') - handle potential invalid month numbers
        monthly_agg['Month_Abbr'] = monthly_agg['Month'].apply(lambda m: calendar.month_abbr[m] if 1 <= m <= 12 else 'Unk')
        monthly_agg['Year-Month-Label'] = monthly_agg['Month_Abbr'] + " " + monthly_agg['Year'].astype(str)
    except Exception as e:
        st.error(f"Error creating month labels: {e}")
        # Fallback label in case of errors
        monthly_agg['Year-Month-Label'] = monthly_agg['Year'].astype(str) + "-" + monthly_agg['Month'].astype(str)

    
    # Check if aggregation results in empty data or only zeros
    if monthly_agg.empty or monthly_agg[metrics_to_plot].sum().sum() == 0:
        # Refine message if date range was applied
        date_msg = f" between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}" if start_date and end_date else ""
        st.info(f"No activity recorded for Rep: {rep_id}{date_msg}.")
        return None

    # --- Plotting --- 
    fig = go.Figure()
    
    # Add bars for each metric using the new 'Year-Month-Label' as x-axis
    for metric in metrics_to_plot:
        display_name = metric_rename_map.get(metric, metric) 
        fig.add_trace(
            go.Bar(
                name=display_name,
                x=monthly_agg['Year-Month-Label'], # Use the new label for x-axis
                y=monthly_agg[metric],
                text=monthly_agg[metric],
                textposition='outside', # Explicitly set text position to outside
                hovertext=[f"{display_name}: {val}" for val in monthly_agg[metric]],
                hoverinfo='text'
            )
        )
    
    # Update layout 
    fig.update_layout(
        #title=title,
        barmode='group',
        xaxis_title="Month", # Keep label simple as 'Month'
        yaxis=dict(
            title="Count"
        ),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10)
        ),
        margin=dict(l=40, r=20, t=60, b=40) 
    )
    
    return fig

def create_activity_summary_table(data, start_date, end_date):
    """
    Create a summary table of activity metrics across all sales reps
    using actual performance data, showing totals, averages, and standard deviations.
    """
    performance_data = data.get('performance_data')
    
    # Check if performance_data exists and is valid
    if performance_data is None or performance_data.empty:
        st.warning("No performance data available to create summary.")
        # Return empty DataFrames with expected columns
        metrics_cols = [
            'Sales Rep', 'Discovery Call', 'F/U Call', 'Email', 'DM Added', 
            'Discovery Visit', 'F/U Visit', 'Demo Scheduled', 'Demo Completed', 'Registration'
        ]
        summary_cols = ['Metric', 'Total', 'Average', 'Standard Deviation']
        top_cols = ['RepName', 'Total Activity'] # Use a different metric for top performers
        
        empty_metrics = pd.DataFrame(columns=metrics_cols)
        empty_summary = pd.DataFrame(columns=summary_cols)
        empty_top = pd.DataFrame(columns=top_cols)
        return empty_summary, empty_metrics, empty_top
        
    # Define the metrics to summarize based on available columns
    available_metrics = [
        "Discovery Call", 
        "F/U Call", 
        "Email", 
        "DM Added",
        "Discovery Visit", 
        "F/U Visit", 
        "Demo Scheduled", 
        "Demo Completed", 
        "Registration"
    ]
    
    # Ensure all expected metrics are present in the performance data
    required_metrics = available_metrics + ['Sales Rep']
    missing_cols = [col for col in required_metrics if col not in performance_data.columns]
    if missing_cols:
        st.warning(f"Performance data is missing required columns for summary: {', '.join(missing_cols)}.")
        # Return empty dataframes as above
        # Corrected list definitions with commas
        metrics_cols = [
            'Sales Rep', 'Discovery Call', 'F/U Call', 'Email', 'DM Added', 
            'Discovery Visit', 'F/U Visit', 'Demo Scheduled', 'Demo Completed', 'Registration'
        ]
        summary_cols = ['Metric', 'Total', 'Average', 'Standard Deviation']
        top_cols = ['RepName', 'Total Activity']
        
        empty_metrics = pd.DataFrame(columns=metrics_cols)
        empty_summary = pd.DataFrame(columns=summary_cols)
        empty_top = pd.DataFrame(columns=top_cols)
        return empty_summary, empty_metrics, empty_top
    
    # Group by Sales Rep and sum the metrics
    metrics_df = performance_data.groupby('Sales Rep')[available_metrics].sum().reset_index()
    
    # Calculate summary statistics
    summary_data = []
    for metric in available_metrics:
        total = metrics_df[metric].sum()
        average = metrics_df[metric].mean()
        std_dev = metrics_df[metric].std()
        summary_data.append({
            'Metric': metric,
            'Total': total,
            'Average': average,
            'Standard Deviation': std_dev
        })
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_data)
    
    # Calculate a simple 'Total Activity' score for ranking top performers
    # You might want a more sophisticated weighting system here
    metrics_df['Total Activity'] = metrics_df[available_metrics].sum(axis=1)
    
    # Get top performers based on Total Activity
    top_performers = metrics_df.sort_values('Total Activity', ascending=False).head(3)
    # Rename 'Sales Rep' to 'RepName' for consistency if needed, assuming 'Sales Rep' holds the name
    top_performers = top_performers.rename(columns={'Sales Rep': 'RepName'})
    top_performers = top_performers[['RepName', 'Total Activity']]
    
    # Return the summary, the detailed metrics per rep, and top performers
    # Ensure metrics_df also has 'RepName' column if 'Sales Rep' is not the name
    # If 'Sales Rep' is the name column, rename it in metrics_df too
    metrics_df = metrics_df.rename(columns={'Sales Rep': 'RepName'})
    
    return summary_df, metrics_df, top_performers

def create_monthly_performance_tables(data, rep_id):
    """
    Create monthly performance tables showing target, actual, completion percentage,
    commission rates and amounts for the entire year (split into two halves)
    """
    # Get rep accounts (AccountID is from the accounts df)
    rep_accounts = data['accounts'][data['accounts']['RepID'] == rep_id]['AccountID'].tolist()

    # Get rep transactions using LCTN_ID
    # --- FIX THIS LINE (around 3067) ---
    rep_transactions = data['transactions'][
        data['transactions']['LCTN_ID'].isin(rep_accounts) # Use LCTN_ID instead of AccountID
    ].copy() # Add copy()

    # Convert to datetime (use TRAN_DT) - Ensure this happens if needed later
    # rep_transactions['TRAN_DT'] = pd.to_datetime(rep_transactions['TRAN_DT']) # Use TRAN_DT

    # Get target info (RepID is name)
    target_info = data['sales_targets'][data['sales_targets']['RepID'] == rep_id]
    if not target_info.empty:
        annual_target = target_info.iloc[0]['BonusThreshold']
    else:
        annual_target = 150000  # Default value if no target found

    # Monthly target is annual target / 12
    monthly_target = annual_target / 12

    # Create dataframes for both halves of the year
    first_half = []
    second_half = []

    # --- Rest of the function generates random data based on the target ---
    # ... (random data generation logic remains the same) ...
    # Generate consistent but randomized monthly data
    try:
        # Use hash of string RepID for seeding, ensuring it's within bounds
        seed_value = abs(hash(rep_id)) % (2**32)
        np.random.seed(seed_value)
    except Exception as e:
        st.error(f"Error creating seed for RepID '{rep_id}': {e}")
        np.random.seed(42) # Fallback seed

    # Month names
    first_half_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    second_half_months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Base rate range: 1.0% to 2.5%
    # Bonus rate range: 1.8% to 3.5%

    # Generate first half data
    for i, month in enumerate(first_half_months):
        # Generate random completion percentage that increases over time
        completion_pct = np.random.uniform(
            max(30, 40 + i * 5),  # Min (increases each month)
            min(85, 50 + i * 7)    # Max (increases each month)
        )

        # Calculate actual based on target and completion
        actual = monthly_target * (completion_pct / 100)

        # Generate rates based on completion
        base_rate = 1.0 + (completion_pct / 100)
        bonus_rate = base_rate + np.random.uniform(0.5, 1.0)

        # Calculate commissions
        base_commission = actual * (base_rate / 100)

        # Only pay bonus commission if at target
        bonus_commission = 0.0  # Default to zero

        # Add to first half data
        first_half.append({
            'Month': month,
            'Target': monthly_target,
            'Actual': actual,
            'Completion %': completion_pct,
            'Base Rate': base_rate,
            'Bonus Rate': bonus_rate,
            'Base Commission': base_commission,
            'Bonus Commission': bonus_commission,
            'Total': base_commission + bonus_commission
        })

    # Generate second half data with higher completion percentages
    for i, month in enumerate(second_half_months):
        # Generate random completion percentage that increases over time
        completion_pct = np.random.uniform(
            max(50, 70 + i * 3),   # Min (increases each month)
            min(120, 90 + i * 5)    # Max (increases each month)
        )

        # Calculate actual based on target and completion
        actual = monthly_target * (completion_pct / 100)

        # Generate rates based on completion
        base_rate = 1.0 + (completion_pct / 200)  # Higher base rate for second half
        bonus_rate = base_rate + np.random.uniform(0.7, 1.5)

        # Calculate commissions
        base_commission = actual * (base_rate / 100)

        # Only pay bonus commission if at target (over 100%)
        bonus_commission = 0.0  # Default to zero

        # Add to second half data
        second_half.append({
            'Month': month,
            'Target': monthly_target,
            'Actual': actual,
            'Completion %': completion_pct,
            'Base Rate': base_rate,
            'Bonus Rate': bonus_rate,
            'Base Commission': base_commission,
            'Bonus Commission': bonus_commission,
            'Total': base_commission + bonus_commission
        })

    # Convert to dataframes
    first_half_df = pd.DataFrame(first_half)
    second_half_df = pd.DataFrame(second_half)

    return first_half_df, second_half_df

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()