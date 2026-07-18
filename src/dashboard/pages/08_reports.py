import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db import get_companies

st.title("📂 Compliance & Annual Reports Vault")

companies_df = get_companies()
search_query = st.selectbox("Search target corporate profiles repository:", options=[""] + list(companies_df['name']))

if not search_query:
    st.info("👋 Select or type a company name to load accessible report links directory.")
else:
    st.markdown(f"### Historical Annual Reports Directory for: **{search_query}**")
    
    # 404 Response simulation data logic table
    reports_repository = [
        {"Year": "FY 2023-24", "Doc_Type": "Annual Report PDF", "Status": 200, "URL": "https://www.bseindia.com/bseplus/AnnualReport/ValidSample1.pdf"},
        {"Year": "FY 2022-23", "Doc_Type": "Annual Report PDF", "Status": 200, "URL": "https://www.bseindia.com/bseplus/AnnualReport/ValidSample2.pdf"},
        {"Year": "FY 2021-22", "Doc_Type": "Annual Report PDF", "Status": 404, "URL": "https://www.bseindia.com/bseplus/AnnualReport/MissingFile.pdf"},
        {"Year": "FY 2020-21", "Doc_Type": "Annual Report PDF", "Status": 200, "URL": "https://www.bseindia.com/bseplus/AnnualReport/ValidSample3.pdf"},
        {"Year": "FY 2019-20", "Doc_Type": "Annual Report PDF", "Status": 404, "URL": "https://www.bseindia.com/bseplus/AnnualReport/MissingFile2.pdf"},
    ]
    
    for report in reports_repository:
        col_year, col_action = st.columns([2, 5])
        with col_year:
            st.markdown(f"**{report['Year']}** ({report['Doc_Type']})")
        with col_action:
            if report['Status'] == 404:
                # Custom requested red status badge for broken links
                st.markdown("<span style='color:white; background-color:#d9534f; padding:3px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>Report unavailable</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"🔗 [Download Clickable BSE PDF Link]({report['URL']})")