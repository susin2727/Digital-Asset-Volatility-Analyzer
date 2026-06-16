import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Crypto Risk Analytics Dashboard",
    layout="wide"
)
# ================= CUSTOM CSS (UI COLOR FIX) =================

st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #0B1220;
    color: #E5E7EB;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #E5E7EB;
}

/* Titles */
h1, h2, h3 {
    color: #38BDF8;
    font-weight: 700;
}

/* Sub text */
p, span, label {
    color: #E5E7EB;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background-color: #111827;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #1E293B;
}

/* Metric labels */
div[data-testid="metric-container"] > label {
    color: #94A3B8 !important;
}

/* Metric values */
div[data-testid="metric-container"] > div {
    color: #38BDF8 !important;
    font-size: 22px;
}

/* Divider */
hr {
    border: 1px solid #1E293B;
}

/* KPI card container */
.kpi-card {
    background-color: #111827;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    height: 140px;
}

/* KPI title */
.kpi-title {
    color: #94A3B8;
    font-size: 14px;
    margin-bottom: 10px;
}

/* KPI value */
.kpi-value {
    color: #38BDF8;
    font-size: 32px;
    font-weight: 700;
}

[data-baseweb="datepicker"] {
    background-color: #0F172A !important;
}

[data-baseweb="datepicker"] input {
    background-color: #0F172A !important;
    color: #FFFFFF !important;
    border: 1px solid #1E293B !important;
}

[data-baseweb="datepicker"] input::placeholder {
    color: #CBD5E1 !important;
}

[data-baseweb="datepicker"] svg {
    fill: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)
# ================= LOAD DATA =================
price_df = pd.read_csv(
    "data/processed_crypto_data.csv",
    parse_dates=["Date"]
)
metrics_df = pd.read_csv("data/crypto_metrics.csv")
# ================= ASSET NAME MAPPING =================
asset_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "ADA": "cardano",
    "DOGE": "dogecoin"
}
reverse_map = {v: k for k, v in asset_map.items()}
# ================= SIDEBAR FILTERS =================
st.sidebar.title("🔍 Filters")
crypto_list = metrics_df["Asset"].tolist()
selected_crypto = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    crypto_list,
    default=crypto_list[:3]
)
min_date = price_df["Date"].min().date()
max_date = price_df["Date"].max().date()
start_date = st.sidebar.date_input("Start Date", min_date, format="YYYY-MM-DD")
end_date = st.sidebar.date_input("End Date", max_date, format="YYYY-MM-DD")
# ================= PREPARE PRICE DATA =================
crypto_columns = [asset_map[c] for c in selected_crypto if c in asset_map]
filtered_price_df = price_df[["Date"] + crypto_columns]
price_long = filtered_price_df.melt(
    id_vars="Date",
    var_name="Asset",
    value_name="Price"
)
price_long["Asset"] = price_long["Asset"].map(reverse_map)
price_long = price_long[
    (price_long["Date"] >= pd.to_datetime(start_date)) &
    (price_long["Date"] <= pd.to_datetime(end_date))
]
filtered_metrics = metrics_df[
    metrics_df["Asset"].isin(selected_crypto)
]
if price_long.empty:
    st.error("❌ No data available for the selected filters")
    st.stop()
# ================= HEADER =================
st.markdown("### Milestone 3 – Visualization Dashboard")
# ================= REQUIREMENTS & OUTPUTS =================
c1, c2 = st.columns(2)
with c1:
    st.subheader("📌 Requirements")
    st.markdown("""
    - Interactive visualizations (Plotly)  
    - Streamlit dashboard  
    - Time-series price analysis  
    - Risk–return evaluation  
    """)

with c2:
    st.subheader("📌 Outputs")
    st.markdown("""
    - Interactive crypto dashboard  
    - Risk metrics & KPIs  
    - Responsive UI  
    """)

st.markdown("---")
st.title("📊 Crypto Risk Analytics Dashboard")
fig = go.Figure()
# ================= CALCULATE VOLATILITY OVER TIME =================
volatility_df = price_df.copy()
volatility_df.set_index("Date", inplace=True)

# Calculate daily returns
returns = volatility_df.pct_change()

# Rolling volatility (30-day)
rolling_vol = returns.rolling(window=30).std()

# Convert to long format
vol_long = rolling_vol.reset_index().melt(
    id_vars="Date",
    var_name="Asset",
    value_name="Volatility"
)

vol_long["Asset"] = vol_long["Asset"].map(reverse_map)
# Filter selected assets & dates
vol_long = vol_long[
    (vol_long["Asset"].isin(selected_crypto)) &
    (vol_long["Date"] >= pd.to_datetime(start_date)) &
    (vol_long["Date"] <= pd.to_datetime(end_date))
]
# ================= PRICE & VOLATILITY TRENDS =================
st.subheader("📈 Price & Volatility Trends")
combined_fig = go.Figure()
# ---- PRICE LINES ----
for asset in price_long["Asset"].unique():
    asset_data = price_long[price_long["Asset"] == asset]

    combined_fig.add_trace(
        go.Scatter(
            x=asset_data["Date"],
            y=asset_data["Price"],
            mode="lines",
            name=f"{asset} Price",
            yaxis="y1"
        )
    )

# ---- VOLATILITY LINES ----
for asset in vol_long["Asset"].unique():
    vol_data = vol_long[vol_long["Asset"] == asset]

    combined_fig.add_trace(
        go.Scatter(
            x=vol_data["Date"],
            y=vol_data["Volatility"],
            mode="lines",
            name=f"{asset} Volatility",
            yaxis="y2",
            line=dict(dash="dot"),
            opacity=0.8
        )
    )

combined_fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="#0E1117",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Price"),
    yaxis2=dict(
        title="Volatility",
        overlaying="y",
        side="right",
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(combined_fig, use_container_width=True)
# ================= RISK–RETURN (FIXED) =================
st.subheader("⚖ Risk–Return Analysis")
# ❗ Size removed to avoid negative-value error
risk_fig = px.scatter(
    filtered_metrics,
    x="Annual Volatility",
    y="Sharpe Ratio",
    color="Asset",
    title="Risk vs Return",
    template="plotly_dark"
)
#important dot size fix
risk_fig.update_traces(marker=dict(size=16,opacity=0.85,line=dict(width=1,color="white")))
risk_fig.update_layout(plot_bgcolor="#0E1117")
st.plotly_chart(risk_fig, use_container_width=True)
# ================= RADAR / SPIDER CHART =================
st.subheader("🕸 dashboard features")
radar_values = [
    filtered_metrics["Annual Volatility"].mean(),
    filtered_metrics["Sharpe Ratio"].mean(),
    1 - filtered_metrics["Annual Volatility"].mean(),
    filtered_metrics["Beta (vs BTC)"].mean(),
    0.7
]

radar_labels = [
    "Risk",
    "Performance",
    "Stability",
    "Market Sensitivity",
    "Adoption"
]
radar_fig = go.Figure()
radar_fig.add_trace(go.Scatterpolar(
    r=radar_values,
    theta=radar_labels,
    fill="toself",
    name="Risk Profile"
))

radar_fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    template="plotly_dark"
)

st.plotly_chart(radar_fig, use_container_width=True)
# ================= KPI METRICS =================
st.subheader("📊 Key Risk Metrics")
avg_vol = filtered_metrics["Annual Volatility"].mean()
avg_sharpe = filtered_metrics["Sharpe Ratio"].mean()
avg_beta = filtered_metrics["Beta (vs BTC)"].mean()
if avg_vol < 0.4:
    risk_level = "Low"
elif avg_vol < 0.7:
    risk_level = "Medium"
else:
    risk_level = "High"

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Annual Volatility</div>
        <div class="kpi-value">{avg_vol:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Sharpe Ratio</div>
        <div class="kpi-value">{avg_sharpe:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Beta vs BTC</div>
        <div class="kpi-value">{avg_beta:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Risk Level</div>
        <div class="kpi-value">Medium</div>
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")
st.success("✅ Milestone 3 Completed – Crypto Risk Analytics Dashboard")
st.markdown("""
<style>
/* FORCE DATE TEXT VISIBILITY – SIDEBAR SAFE */
section[data-testid="stSidebar"] [data-baseweb="input"] input {
    color: black !important;
    background-color: white !important;
}
</style>
""", unsafe_allow_html=True)