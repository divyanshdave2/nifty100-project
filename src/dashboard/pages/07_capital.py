import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.title("🗺️ Capital Allocation Matrix Map")

# Group 92 companies into 8 allocation patterns
patterns = ["Aggressive CapEx", "Conservative Cash Pile", "Heavy R&D Drive", "High Dividend Payout", "Debt Reduction Focus", "M&A Execution", "Share Buyback Intensive", "Balanced Reinvestment"]

np.random.seed(101)
company_names = [f"Nifty Company {i:02d}" for i in range(1, 93)]
assigned_patterns = np.random.choice(patterns, 92)
market_caps = np.random.uniform(10000, 600000, 92)

treemap_df = pd.DataFrame({
    "Total_Universe": ["Nifty 100 System"] * 92,
    "Allocation_Pattern": assigned_patterns,
    "Company_Name": company_names,
    "Market_Cap": market_caps
})

st.markdown("#### 🪵 Pattern Grouping Tree Engine")
fig_tree = px.treemap(
    treemap_df, path=["Total_Universe", "Allocation_Pattern", "Company_Name"],
    values="Market_Cap", color="Allocation_Pattern", title="Treemap Distribution of 92 Companies Across 8 Allocation Patterns"
)
st.plotly_chart(fig_tree, use_container_width=True)

# Click-action mock selection pipeline
st.markdown("---")
st.markdown("#### 🔍 Filter Directory by Patterns Allocation Layer")
chosen_pattern = st.selectbox("Click/Select a pattern to view all associated companies:", options=patterns)
filtered_cos = treemap_df[treemap_df['Allocation_Pattern'] == chosen_pattern][['Company_Name', 'Market_Cap']]
st.dataframe(filtered_cos.sort_values(by="Market_Cap", ascending=False), hide_index=True, use_container_width=True)