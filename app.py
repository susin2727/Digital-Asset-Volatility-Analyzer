import streamlit as st
import plotly.express as px
import numpy as np
from utils import fetch_crypto_data, calculate_metrics

# Page config
st.set_page_config(
    page_title="Crypto Volatility & Risk Analyzer",
    layout="wide"
)

st.title("📊 Crypto Volatility & Risk Analyzer")

# User Inputs
crypto = st.selectbox(
    "Select Cryptocurrency",
    ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]
)

days = st.slider(
    "Select number of days",
    min_value=30,
    max_value=365,
    value=90
)

# Fetch Data
df = fetch_crypto_data(crypto, days)

# Calculate Metrics
volatility, sharpe = calculate_metrics(df)

# Metrics Display
col1, col2 = st.columns(2)
col1.metric("Annualized Volatility", f"{volatility:.2f}")
col2.metric("Sharpe Ratio", f"{sharpe:.2f}")

# Price Trend Chart
fig_price = px.line(
    df,
    x="date",
    y="price",
    title=f"{crypto.upper()} Price Trend"
)
st.plotly_chart(fig_price, use_container_width=True)

# Rolling Volatility
df["rolling_volatility"] = df["returns"].rolling(7).std() * np.sqrt(365)

fig_vol = px.line(
    df,
    x="date",
    y="rolling_volatility",
    title="7-Day Rolling Volatility"
)
st.plotly_chart(fig_vol, use_container_width=True)

# Risk Classification
def classify_risk(vol):
    if vol > 0.8:
        return "🔴 High Risk"
    elif vol > 0.4:
        return "🟠 Medium Risk"
    else:
        return "🟢 Low Risk"

risk_level = classify_risk(volatility)

st.subheader(f"Risk Level: {risk_level}")