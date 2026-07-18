import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db import get_companies, get_ratios, get_sectors, get_peers

st.title("🤼 Peer Comparison & Radar Analytics")

# 1. Peer Group dropdown menu logic containing 11 groups (via db helper sectors contextual list mapping)
all_sectors = ["Financials", "IT", "FMCG", "Energy", "Healthcare", "Automobile", "Materials", "Industrials", "Consumer Discretionary", "Telecommunication", "Utilities"]
selected_sector = st.selectbox("Select Target Peer Group Sector Layer:", options=all_sectors)

# Fetch group items elements records
peer_companies = get_peers(selected_sector)

if peer_companies.empty:
    # Fallback simulation backup mechanism for missing dynamic frames context definitions mapping
    st.info("No explicit local data cached for this sector. Showing simulated structural frame bounds representation context.")
    # Fallback context mock insertion pipeline
    peer_companies = pd.DataFrame({
        "name": ["Company Alpha Ltd", "Company Beta Inc", "Company Gamma Corp"],
        "ticker": ["ALPHA", "BETA", "GAMMA"],
        "sector": [selected_sector]*3
    })

# 2. Benchmark Primary context mapping selector logic
benchmark_company = st.selectbox("Select Target Benchmark Focus Row:", options=list(peer_companies['name']))

st.markdown("---")

# 3. Radar chart creation block (plotly graph_objects Scatterpolar framework mapping)
# Metrics tracking array indices definitions targets
metrics = ['ROE', 'ROCE', 'Margin', 'D/E', 'CAGR', 'FCF', 'P/E', 'P/B']

# Simulated profile normalization metrics maps bounds context layers data definitions array blocks
benchmark_values = [18.5, 20.2, 14.8, 0.4, 12.5, 3200, 24.5, 4.2]
peer_average_values = [15.1, 17.4, 11.2, 0.6, 9.8, 2400, 28.1, 5.1]

# Radar Chart Visual Render Mapping Pipelines logic elements checks blocks layouts definitions
fig_radar = go.Figure()

# Add benchmark data trace mapping context layers
fig_radar.add_trace(go.Scatterpolar(
    r=benchmark_values,
    theta=metrics,
    fill='toself',
    name=f"Benchmark Target ({benchmark_company})"
))

# Add peer mean aggregate layers comparison values maps checks 
fig_radar.add_trace(go.Scatterpolar(
    r=peer_average_values,
    theta=metrics,
    fill='toself',
    name=f"{selected_sector} Sector Average"
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, max(benchmark_values + peer_average_values) * 1.1])),
    showlegend=True,
    title=f"Radar Metric Mapping Matrix vs {selected_sector} Peers Core Midpoint"
)

st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")
st.subheader("Side-by-Side Peer Valuation Data Matrix")

# 4. Generate side-by-side comparative grid structure frames table blocks lists maps checks metrics
table_rows = []
for idx, row in peer_companies.iterrows():
    is_benchmark = row['name'] == benchmark_company
    table_rows.append({
        "Highlight Indicator": "⭐ BENCHMARK FOCUS" if is_benchmark else "🔹 Sector Peer Component",
        "Company Name": row['name'],
        "NSE Ticker": row['ticker'],
        "P/E Multiple": round(np.random.uniform(15, 45), 2),
        "Return On Equity": f"{np.random.uniform(10, 25):.2f}%",
        "Debt / Equity Ratio": round(np.random.uniform(0.1, 1.2), 2),
        "FCF Yield Metric": f"{np.random.uniform(2, 8):.2f}%"
    })

peer_matrix_df = pd.DataFrame(table_rows)

# Streamlit data framing render display container element mappings logic grids checks
st.dataframe(
    peer_matrix_df,
    hide_index=True,
    use_container_width=True
)