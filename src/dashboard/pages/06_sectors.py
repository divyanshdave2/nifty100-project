import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.title("📊 Sector Dynamics Workspace")

all_sectors = ["Financials", "IT", "FMCG", "Energy", "Healthcare", "Automobile", "Materials"]
selected_sector = st.selectbox("Select Target Sector View:", options=all_sectors)

# Bubble Chart: X=Revenue, Y=ROE, Size=Market Cap, Color=Sub-sector
np.random.seed(42)
mock_companies = [f"Company {chr(65+i)}" for i in range(15)]
mock_subsectors = ["Sub-Sector Alpha", "Sub-Sector Beta", "Sub-Sector Gamma"]

sector_data = pd.DataFrame({
    "Company": mock_companies,
    "Sub_Sector": np.random.choice(mock_subsectors, 15),
    "Revenue": np.random.uniform(10000, 95000, 15),
    "ROE": np.random.uniform(8, 28, 15),
    "Market_Cap": np.random.uniform(5000, 500000, 15)
})

st.markdown("#### 🫧 Multi-Dimensional Sector Bubble Chart")
fig_bubble = px.scatter(
    sector_data, x="Revenue", y="ROE", size="Market_Cap", color="Sub_Sector",
    hover_name="Company", size_max=50, title=f"Landscape Structure inside {selected_sector}"
)
st.plotly_chart(fig_bubble, use_container_width=True)

# Sector Median KPI Bar Chart below
st.markdown("#### 🏛️ Sector Median KPI Benchmarks")
kpi_medians = pd.DataFrame({
    "Metric Benchmark": ["Sector Median ROE (%)", "Sector Median ROCE (%)", "Sector Median NPM (%)", "Sector Median D/E"],
    "Value": [15.4, 17.1, 12.3, 0.45]
})
fig_bar = px.bar(kpi_medians, x="Metric Benchmark", y="Value", color="Metric Benchmark", text_auto=True)
st.plotly_chart(fig_bar, use_container_width=True)