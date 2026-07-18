import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db import get_companies, get_ratios

st.title("📈 Trend Analysis Layer")

companies_df = get_companies()
selected_company = st.selectbox("Select Company for Historical Trend Tracking:", options=list(companies_df['name']))
ticker = companies_df[companies_df['name'] == selected_company]['ticker'].values[0]

# Multi-metric selector (Overlay up to 3 metrics)
all_metrics = {"ROE (%)": "roe", "ROCE (%)": "roce", "Net Profit Margin (%)": "net_profit_margin", "Debt/Equity": "de", "Interest Coverage": "icr"}
selected_labels = st.multiselect("Select Metrics to Overlay (Max 3):", options=list(all_metrics.keys()), default=["ROE (%)", "ROCE (%)"])

if len(selected_labels) > 3:
    st.error("⚠️ Maximum threshold reached! Please select up to 3 metrics only.")
elif len(selected_labels) == 0:
    st.warning("👋 Please select at least one metric to visualize the trend line.")
else:
    ratios_df = get_ratios(ticker).sort_values(by="year")
    
    fig = go.Figure()
    for label in selected_labels:
        metric_col = all_metrics[label]
        y_vals = ratios_df[metric_col].values
        years = ratios_df['year'].values
        
        # Add primary metric line trace
        fig.add_trace(go.Scatter(mode='lines+markers', x=years, y=y_vals, name=label))
        
        # YoY % Change Annotations calculation
        for i in range(1, len(y_vals)):
            prev = y_vals[i-1]
            curr = y_vals[i]
            if prev != 0:
                yoy_change = ((curr - prev) / abs(prev)) * 100
                sign = "+" if yoy_change >= 0 else ""
                fig.add_annotation(
                    x=years[i], y=curr,
                    text=f"{sign}{yoy_change:.1f}%",
                    showarrow=False, yshift=12,
                    font=dict(size=9, color="green" if yoy_change >= 0 else "red")
                )
                
    fig.update_layout(title=f"10-Year Historical Trends Matrix for {selected_company}", xaxis_title="Financial Year", yaxis_title="Metric Value / Percentage")
    st.plotly_chart(fig, use_container_width=True)