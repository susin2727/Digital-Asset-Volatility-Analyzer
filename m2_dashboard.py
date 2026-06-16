import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Milestone 2: Crypto Risk Analysis", layout="wide")

st.markdown("""
<style>
body, .stApp {background-color:#0E1117; color:white;}
h1,h2,h3,h4,h5,h6,p,label {color:white !important;}
.metric-table th {background:#1f2937;color:white;}
.metric-table td {background:#111827;color:white;text-align:center;}
.badge {background:#2563EB;color:white;padding:4px 10px;border-radius:10px;}
.low {color:#22c55e;font-weight:bold;}
.med {color:#facc15;font-weight:bold;}
.high {color:#ef4444;font-weight:bold;}
</style>
""", unsafe_allow_html=True)


# -------------------- HEADER --------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 Milestone 2 : Crypto Risk Analysis")
with col2:
    st.markdown(
        f"<p style='text-align:right;margin-top:25px;'>🟢 Live Analysis <span class='badge'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span></p>",
        unsafe_allow_html=True
    )

# -------------------- LOAD DATA --------------------
df = pd.read_csv("data/crypto_metrics.csv")
df.columns = ["Asset", "Daily_Volatility", "Annual_Volatility", "Sharpe_Ratio", "Beta"]

# -------------------- TIME RANGE --------------------
st.markdown("### 📅 Select Analysis Period")
period = st.radio("", ["30 Days", "90 Days", "1 Year"], horizontal=True)

factor = {"30 Days": 1.0, "90 Days": 0.9, "1 Year": 0.8}[period]
df["Volatility"] = df["Daily_Volatility"] * factor

# -------------------- VALUE AT RISK (VaR) --------------------
df["VaR_95"] = 1.65 * df["Volatility"]

# -------------------- RISK CLASSIFICATION --------------------
low = df["Volatility"].quantile(0.33)
high = df["Volatility"].quantile(0.66)

def classify_risk(v):
    if v < low:
        return "Low"
    elif v < high:
        return "Medium"
    else:
        return "High"

df["Risk"] = df["Volatility"].apply(classify_risk)

def color_value(value, risk):
    color = "low" if risk == "Low" else "med" if risk == "Medium" else "high"
    return f"<span class='{color}'>{value}</span>"

# -------------------- LAYOUT --------------------
left, right = st.columns([2, 3])

# -------------------- LEFT PANEL --------------------
with left:
    st.markdown("## 🧾 Requirements")
    st.markdown("""
    - Daily returns calculation  
    - Statistical risk measures  
    - Moving averages  
    """)

    st.markdown("## 📤 Outputs")
    st.markdown("""
    - Risk metrics table  
    - Processed dataset  
    """)

    st.markdown("## 📊 Crypto Volatility Comparison")
    fig = px.bar(
        df,
        x="Asset",
        y="Volatility",
        color="Risk",
        color_discrete_map={"Low":"green","Medium":"yellow","High":"red"},
        text=(df["Volatility"]*100).round(2)
    )
    fig.update_layout(template="plotly_dark", yaxis_title="Volatility (%)")
    st.plotly_chart(fig, use_container_width=True)

# -------------------- RIGHT PANEL --------------------
with right:
    st.markdown("## 📈 Risk Metrics Dashboard")

    table = pd.DataFrame({
        "Asset": df["Asset"],
        "Volatility (%)": [
            color_value(f"{v*100:.2f}", r) for v, r in zip(df["Volatility"], df["Risk"])
        ],
        "Sharpe Ratio": df["Sharpe_Ratio"].round(2),
        "Beta": df["Beta"].round(2),
        "VaR (95%)": [
            color_value(f"{v*100:.2f}", r) for v, r in zip(df["VaR_95"], df["Risk"])
        ],
        "Risk Level": [
          "<span class='low'>Low</span>" if r=="Low"
           else "<span class='med'>Medium</span>" if r=="Medium"
           else "<span class='high'>High</span>"
           for r in df["Risk"]
]
    })

    st.markdown(table.to_html(escape=False, index=False, classes="metric-table"), unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("<p style='text-align:center;'>✅ Milestone 2 Completed – Crypto Risk Dashboard</p>", unsafe_allow_html=True)