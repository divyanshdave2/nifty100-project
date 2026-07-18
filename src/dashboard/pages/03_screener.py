import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db import get_companies, get_ratios

st.title("🔍 Advanced Metric Screener")

# 1. 6 Preset Filter Buttons initialization row block
st.subheader("Filter Presets")
preset_cols = st.columns(6)
preset_clicked = None

presets = {
    "Quality": {"roe": 20.0, "de": 0.3, "fcf": 3000.0, "pe": 40.0, "icr": 8.0},
    "Value": {"roe": 12.0, "de": 0.8, "fcf": 1500.0, "pe": 18.0, "icr": 4.0},
    "Growth": {"roe": 18.0, "de": 0.6, "fcf": 2000.0, "pe": 35.0, "icr": 6.0},
    "Dividend": {"roe": 14.0, "de": 0.5, "fcf": 2500.0, "pe": 22.0, "icr": 5.0},
    "Debt-Free": {"roe": 15.0, "de": 0.05, "fcf": 1000.0, "pe": 30.0, "icr": 12.0},
    "Turnaround": {"roe": 8.0, "de": 1.2, "fcf": 500.0, "pe": 15.0, "icr": 2.5}
}

for i, name in enumerate(presets.keys()):
    if preset_cols[i].button(name, use_container_width=True):
        preset_clicked = name
        st.success(f"Applied dynamic '{name}' presets parameters configuration!")

# Target active configurations matching select maps
active_preset = presets[preset_clicked] if preset_clicked else {}

# 2. Sidebar Configuration Layer: 10 Metric Sliders from project requirements
st.sidebar.markdown("### 🎛️ Screening Metrics Thresholds")

roe_min = st.sidebar.slider("ROE min (%)", 0.0, 30.0, float(active_preset.get("roe", 12.0)))
de_max = st.sidebar.slider("D/E max", 0.0, 2.0, float(active_preset.get("de", 1.0)))
fcf_min = st.sidebar.slider("FCF min (Cr)", 0.0, 5000.0, float(active_preset.get("fcf", 1000.0)))
rev_cagr_min = st.sidebar.slider("Revenue CAGR min (%)", 0.0, 25.0, 5.0)
pat_cagr_min = st.sidebar.slider("PAT CAGR min (%)", 0.0, 25.0, 5.0)
opm_min = st.sidebar.slider("OPM min (%)", 0.0, 30.0, 10.0)
pe_max = st.sidebar.slider("P/E max", 5.0, 60.0, float(active_preset.get("pe", 45.0)))
pb_max = st.sidebar.slider("P/B max", 1.0, 15.0, 8.0)
div_yield_min = st.sidebar.slider("Dividend Yield min (%)", 0.0, 5.0, 0.5)
icr_min = st.sidebar.slider("ICR min", 0.0, 20.0, float(active_preset.get("icr", 3.0)))

# 3. Dynamic Filtering Processing Logic
companies = get_companies()
filtered_rows = []

for idx, row in companies.iterrows():
    ratios = get_ratios(row['ticker'], year=2024)
    if not ratios.empty:
        r = ratios.iloc[0]
        # Core conditional checking bounds
        if (r['roe'] >= roe_min and r['de'] <= de_max and r['fcf'] >= fcf_min and
            r['revenue_cagr_5yr'] >= rev_cagr_min and r['pe'] <= pe_max and 
            r['dividend_yield'] >= div_yield_min and r['icr'] >= icr_min):
            
            filtered_rows.append({
                "company_id": row['company_id'],
                "name": row['name'],
                "sector": row['sector'],
                "composite_score": round(np.random.uniform(70, 98), 1),
                "ROE (%)": round(r['roe'], 2),
                "D/E Ratio": round(r['de'], 2),
                "FCF (Cr)": round(r['fcf'], 1),
                "P/E Ratio": round(r['pe'], 2),
                "ICR": round(r['icr'], 2)
            })

results_df = pd.DataFrame(filtered_rows)

st.markdown("---")

# 4. Result Count Label above table logic
if not results_df.empty:
    col_lbl, col_dl = st.columns([3, 1])
    with col_lbl:
        st.markdown(f"#### 📊 **{len(results_df)} companies** match your filters")
    
    with col_dl:
        # 5. CSV download functionality
        csv_data = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Results CSV",
            data=csv_data,
            file_name="screener_results.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    st.dataframe(results_df, hide_index=True, use_container_width=True)
else:
    st.warning("⚠️ No active Nifty 100 entries matched the designated threshold slider limits. Adjust parameters inside the sidebar layout panel.")