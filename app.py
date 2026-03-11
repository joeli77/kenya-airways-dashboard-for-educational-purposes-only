import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Kenya Airways Dashboard", layout="wide")

st.title("Kenya Airways – Executive Financial Dashboard")

st.caption(
    "Verified Actuals Mode | FY2024 base results | HY2025 interim update | Educational use"
)

st.header("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue FY2024", "KSh 188.5bn", "+6%")
col2.metric("Operating Profit", "KSh 16.6bn", "+58%")
col3.metric("Profit After Tax", "KSh 5.4bn", "Return to profit")
col4.metric("Passengers", "5.23M", "+4%")

data = pd.DataFrame({
    "Year": ["FY2023", "FY2024"],
    "Revenue": [177, 188.5],
    "Operating Profit": [10.5, 16.6]
})

fig = px.bar(
    data,
    x="Year",
    y=["Revenue", "Operating Profit"],
    barmode="group",
    title="Revenue vs Operating Profit"
)

st.plotly_chart(fig, use_container_width=True)

st.header("Operating Metrics")

ops = pd.DataFrame({
    "Metric": ["Passengers (M)", "Cabin Factor (%)"],
    "FY2023": [5.0, 73.5],
    "FY2024": [5.23, 75.2]
})

st.dataframe(ops, use_container_width=True)

st.header("HY2025 Interim Update")

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", "KSh 75bn", "-19%")
col2.metric("Passenger Change", "-14%")
col3.metric("Operating Result", "-KSh 6.2bn")

st.warning(
    "HY2025 reflects lower traffic and grounded aircraft. "
    "Interim performance is not directly comparable to FY2024."
)

st.header("Sources")

st.write("""
Kenya Airways FY2024 Results  
Kenya Airways Annual Report  
Kenya Airways HY2025 Interim Update
""")

st.caption(f"Last updated {datetime.now().date()}")
