import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db import get_companies, get_ratios, get_pl

st.title("🏢 Company Profile Analytics")

# 1. Company List fetch karein for auto-complete dropdown text selector
companies_df = get_companies()
search_options = list(companies_df['name']) + list(companies_df['ticker'])

# Autocomplete text search component box setup
selected_input = st.selectbox(
    "Search Company Name or NSE Ticker Symbol:",
    options=[""] + search_options,
    index=0,
    placeholder="Type to search e.g., RELIANCE or TCS..."
)

# 2. Friendly Error Catching Engine: Block details processing when entry missing or incorrect
if not selected_input:
    st.info("👋 Please enter or select a valid company name or ticker symbol from the search box above to populate dashboard analytics layouts.")
else:
    # Resolve valid record context matching row elements
    matched_row = companies_df[
        (companies_df['name'] == selected_input) | (companies_df['ticker'] == selected_input)
    ]
    
    if matched_row.empty:
        # Error handling message mapping from requirements specs
        st.error("❌ Ticker not found – please try another")
    else:
        # Pull records meta targets maps
        company = matched_row.iloc[0]
        ticker = company['ticker']
        
        # A. Company Profile Main Card Display Component Block
        st.markdown(f"## {company['name']} ({ticker})")
        
        card_col1, card_col2, card_col3 = st.columns(3)
        with card_col1:
            st.markdown(f"**Sector:** {company['sector']}")
        with card_col2:
            st.markdown(f"**Sub-Sector:** {company['sub_sector']}")
        with card_col3:
            st.markdown(f"**NSE Ticker Code:** {ticker}")
            
        st.caption(f"**Company Profile:** {company['description']}")
        st.markdown("---")
        
        # Fetching actual dynamic system ratios
        ratios_history = get_ratios(ticker)
        latest_ratio = ratios_history.sort_values(by="year", ascending=False).iloc[0]
        
        # B. Render 6 specialized KPI individual tiles
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
        kpi1.metric("ROE (%)", f"{latest_ratio['roe']:.2f}%")
        kpi2.metric("ROCE (%)", f"{latest_ratio['roce']:.2f}%")
        kpi3.metric("Net Profit Margin", f"{latest_ratio['net_profit_margin']:.2f}%")
        kpi4.metric("D/E Ratio", f"{latest_ratio['de']:.2f}")
        kpi5.metric("Revenue CAGR 5yr", f"{latest_ratio['revenue_cagr_5yr']:.2f}%")
        kpi6.metric("FCF (Latest Year Cr)", f"₹{latest_ratio['fcf']:.0f}")
        
        st.markdown("---")
        
        # Charts section layouts configurations grid split maps
        chart_col1, chart_col2 = st.columns(2)
        
        # C. 10-Year Bar Chart for Revenue and Net Profit using Plotly
        with chart_col1:
            st.markdown("#### 📊 10-Year Financial Trajectory (Revenue & Profits)")
            pl_df = get_pl(ticker)
            
            fig_bar = px.bar(
                pl_df, 
                x="year", 
                y=["Revenue", "Net_Profit"],
                barmode="group",
                labels={"value": "Amount (in Crores)", "year": "Financial Year"},
                color_discrete_sequence=["#1f77b4", "#2ca02c"]
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        # D. ROE & ROCE Dual-Axis Line Chart tracking trends pattern
        with chart_col2:
            st.markdown("#### 📈 ROE vs ROCE Dual-Axis Trend Tracking")
            
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=ratios_history['year'], y=ratios_history['roe'],
                mode='lines+markers', name='ROE (%)', line=dict(color='blue')
            ))
            fig_line.add_trace(go.Scatter(
                x=ratios_history['year'], y=ratios_history['roce'],
                mode='lines+markers', name='ROCE (%)', line=dict(color='orange')
            ))
            fig_line.update_layout(
                xaxis_title="Year",
                yaxis_title="Percentage (%)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_line, use_container_width=True)
            
        st.markdown("---")
        
        # E. Pros & Cons Sections UI Render indicators Engine layout mapping
        pros_col, cons_col = st.columns(2)
        with pros_col:
            st.markdown("#### 🟢 Pro Factors Analysis")
            st.markdown("✅ Consistent strong operational efficiency metrics return models.")
            st.markdown("✅ Healthy interest coverage ratios safely maintaining headroom liquidity.")
            st.markdown("✅ Working capital lifecycle optimization cycles decreasing run overhead.")
            
        with cons_col:
            st.markdown("#### 🔴 Con Risk Factors Assessment")
            st.markdown("❌ High sectoral valuation multiple pricing premiums over trailing levels.")
            st.markdown("❌ Marginal inventory pileups visible in near-term rolling asset checks.")