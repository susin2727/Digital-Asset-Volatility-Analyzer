import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# ============================================
# CUSTOM FULL UI THEME 
# ============================================

custom_css = """
<style>

body {
    background: linear-gradient(135deg, #0A0F24, #0E162E) !important;
    color: white !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0A0F24, #0E162E) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.card-box {
    padding: 25px;
    border-radius: 18px;
    background: rgba(22, 27, 34, 0.75);
    border: 1px solid #1F2937;
    box-shadow: 0 0 25px rgba(0, 150, 255, 0.08);
    margin-bottom: 20px;
}

.refresh-btn {
    background-color: #1E60FF !important;
    color: white !important;
    padding: 10px 25px !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

h1, h2, h3, h4, h5 {
    color: #58A6FF !important;
    font-weight: 700 !important;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.markdown("#  Milestone 1: Data Acquisition")
st.markdown("### Live Crypto Data Fetcher Dashboard")

left, right = st.columns([1, 2])

# Left side panels
with left:
    
    st.subheader("📌 Requirements")
    st.markdown("""
    - Environment Setup (Python)
    - API Integration (CoinGecko)
    - Data Storage (CSV format)
    - Preprocessing missing values
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    
    st.subheader("📦 Outputs")
    st.markdown("""
    - Daily price data for 8+ cryptocurrencies  
    - Verified API connectivity  
    - Trend charts (BTC, ETH, SOL)
    """)
    st.markdown("</div>", unsafe_allow_html=True)


 
    st.subheader("🔵 Crypto Data Fetcher  •  Live")

    # Refresh button
    refresh = st.button("🔄 Refresh Data", key="refresh", help="Fetch latest crypto values")

    # Show live updated timestamp
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    st.markdown(f"#### 🕒 Last Updated: *{now}*")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# FETCH LIVE DATA
# ============================================

coins = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin", "litecoin", "ripple", "polkadot"]

def fetch_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    return requests.get(url, params=params).json()

data = fetch_data()

# ============================================
# LIVE TABLE
# ============================================

rows = []
for coin in coins:
    price = data[coin]["usd"]
    change = data[coin]["usd_24h_change"]
    volume = data[coin]["usd_24h_vol"]

    arrow = "📈" if change >= 0 else "📉"

    rows.append([
        coin.title(),
        f"${price:,.2f}",
        f"{arrow} {change:.2f}%",
        f"${volume/1_000_000_000:.2f}B"
    ])

df = pd.DataFrame(rows, columns=[
    "Cryptocurrency", "Price (USD)", "24h Change", "Volume (24h)"
])


st.dataframe(df, use_container_width=True, height=380)
st.markdown("</div>", unsafe_allow_html=True)


# ============================================
# 7-DAY TREND CHARTS
# ============================================

st.markdown("## 📈 7-Day Price Trend")

hist_url = "https://api.coingecko.com/api/v3/coins/{}/market_chart"
trend = {}

for coin in ["bitcoin", "ethereum", "solana"]:
    r = requests.get(hist_url.format(coin), params={"vs_currency": "usd", "days": 7}).json()
    trend[coin] = [p[1] for p in r["prices"]]

fig1 = go.Figure()
fig1.add_trace(go.Scatter(y=trend["bitcoin"], mode="lines+markers", name="BTC"))
fig1.add_trace(go.Scatter(y=trend["ethereum"], mode="lines+markers", name="ETH"))
fig1.update_layout(template="plotly_dark", title="BTC & ETH 7-Day Trend")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(y=trend["solana"], mode="lines+markers", name="SOL"))
fig2.update_layout(template="plotly_dark", title="Solana 7-Day Trend")

c1, c2 = st.columns(2)
c1.plotly_chart(fig1, use_container_width=True)
c2.plotly_chart(fig2, use_container_width=True)
# VOLUME CHART
# ============================================

st.markdown("## 📊 24h Trading Volume")

volume_values = [data[c]["usd_24h_vol"] for c in coins]

fig3 = go.Figure([go.Bar(x=[c.title() for c in coins], y=volume_values)])
fig3.update_layout(template="plotly_dark", title="24h Trading Volume")

st.plotly_chart(fig3, use_container_width=True)

