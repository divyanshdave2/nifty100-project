import streamlit as st
import plotly.express as px
import pandas as pd
# Root directory utilities handle se import karne ke liye path add module check
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db import get_companies, get_ratios

st.title("🏠 Home Overview - Nifty 100 Analytics")

# 1. Sidebar me Year Selector (2019 to 2024) - dynamically re-loads all values
st.sidebar.markdown("### Home Screen Controls")
selected_year = st.sidebar.selectbox("Select Financial Year", options=[2024, 2023, 2022, 2021, 2020, 2019], key="home_year_selector")

st.markdown(f"Showing analytical aggregates for Financial Year: **{selected_year}**")

# Mock processing calculations base on year selector update simulation
# In production, data updates filter using get_ratios(ticker, year=selected_year)
kpi_data = {
    2024: {"roe": "16.4%", "pe": "24.2", "de": "0.45", "companies": "92", "cagr": "11.2%", "debt_free": "18"},
    2023: {"roe": "15.8%", "pe": "22.9", "de": "0.48", "companies": "92", "cagr": "10.9%", "debt_free": "16"},
    2022: {"roe": "14.2%", "pe": "25.1", "de": "0.51", "companies": "90", "cagr": "9.8%", "debt_free": "14"},
    2021: {"roe": "13.9%", "pe": "28.4", "de": "0.55", "companies": "89", "cagr": "8.5%", "debt_free": "11"},
    2020: {"roe": "12.1%", "pe": "19.8", "de": "0.58", "companies": "88", "cagr": "7.2%", "debt_free": "10"},
    2019: {"roe": "14.5%", "pe": "23.4", "de": "0.52", "companies": "88", "cagr": "10.1%", "debt_free": "15"},
}
current_metrics = kpi_data[selected_year]

# 2. Render 6 Summary KPI tiles at the top
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Average ROE", current_metrics["roe"])
col2.metric("Median P/E", current_metrics["pe"])
col3.metric("Median D/E", current_metrics["de"])
col4.metric("Total Companies", current_metrics["companies"])
col5.metric("Median Revenue CAGR 5yr", current_metrics["cagr"])
col6.metric("Debt-Free Companies", current_metrics["debt_free"])

st.markdown("---")

# Layout Split into Columns
left_chart, right_table = st.columns([1, 1])

with left_chart:
    st.markdown("#### 🍩 Sector Breakdown Count")
    # 3. Sector breakdown donut chart using Plotly (11 sectors representation)
    sector_counts = pd.DataFrame({
        "Sector": ["Financials", "IT", "FMCG", "Energy", "Healthcare", "Automobile", "Materials", "Industrials", "Consumer Discretionary", "Telecommunication", "Utilities"],
        "Company Count": [25, 16, 12, 10, 8, 7, 5, 4, 2, 2, 1]
    })
    
    fig_donut = px.pie(
        sector_counts, 
        names="Sector", 
        values="Company Count", 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_donut, use_container_width=True)

with right_table:
    st.markdown("#### 🏆 Top-5 Companies by Composite Quality Score")
    # 4. Top-5 companies table
    companies = get_companies()
    # Adding mock score mapping for preview layout sorting
    companies['Composite Score'] = [94.5, 91.2, 89.8, 88.5, 87.2]
    top_5_df = companies.sort_values(by="Composite Score", ascending=False).head(5)
    
    st.dataframe(
        top_5_df[['name', 'ticker', 'sector', 'Composite Score']], 
        hide_index=True, 
        use_container_width=True
    )