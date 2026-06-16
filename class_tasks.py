# -----------------------------
# INSTALL REQUIRED PACKAGES
# ------------------------------
import requests
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# ============================================================
# TASK 1 → Fetch live data for 8 cryptocurrencies
# ============================================================

coins = [
    "bitcoin", "ethereum", "solana", "cardano", "dogecoin",
    "litecoin", "ripple", "polkadot"
]

url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": ",".join(coins),
    "vs_currencies": "usd",
    "include_24hr_vol": "true",
    "include_24hr_change": "true"
}

data = requests.get(url, params=params).json()

# ============================================================
# TASK 2 → Format table + add 📈 or 📉 arrows
# ============================================================

rows = []

for coin in coins:
    price = data[coin]["usd"]
    change = data[coin]["usd_24h_change"]
    volume = data[coin]["usd_24h_vol"]

    # Add arrow symbol
    if change >= 0:
        change_symbol = f"📈 {change:.2f}%"
    else:
        change_symbol = f"📉 {change:.2f}%"

    rows.append([
        coin.title(),
        f"${price:,.2f}",
        change_symbol,
        f"${volume/1_000_000_000:.2f}B"
    ])

df = pd.DataFrame(rows, columns=["Cryptocurrency", "Price", "24h Change", "Volume (24h)"])

print("\n🔵 LIVE CRYPTO PRICE TABLE\n")
print("Last updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
df

# ============================================================
# TASK 3 → Fetch 7-day history for BTC, ETH, and SOLANA
# ============================================================

hist_url = "https://api.coingecko.com/api/v3/coins/{}/market_chart"
trend = {}

for coin in ["bitcoin", "ethereum", "solana"]:
    r = requests.get(hist_url.format(coin), params={"vs_currency": "usd", "days": 7}).json()
    trend[coin] = [p[1] for p in r["prices"]]

# ============================================================
# TASK 4 → Add last updated time to graph title
# ============================================================

last_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# BTC + ETH Graph
fig1 = go.Figure()
fig1.add_trace(go.Scatter(y=trend["bitcoin"], mode="lines+markers", name="BTC"))
fig1.add_trace(go.Scatter(y=trend["ethereum"], mode="lines+markers", name="ETH"))

fig1.update_layout(
    title=f"7-Day Price Trend (BTC & ETH) — Updated: {last_time}",
    xaxis_title="Day",
    yaxis_title="Price (USD)",
    template="plotly_dark",
    height=420
)

fig1.show()

# ============================================================
# TASK 3 (part 2) → Solana-only separate chart
# ============================================================

fig2 = go.Figure()
fig2.add_trace(go.Scatter(y=trend["solana"], mode="lines+markers", name="Solana (SOL)"))

fig2.update_layout(
    title=f"7-Day Solana (SOL) Trend — Updated: {last_time}",
    xaxis_title="Day",
    yaxis_title="Price (USD)",
    template="plotly_dark",
    height=420
)

fig2.show()

# ============================================================
# BONUS TASK → Bar chart of 24h volume
# ============================================================

volume_values = [data[c]["usd_24h_vol"] for c in coins]

fig3 = go.Figure([go.Bar(x=[c.title() for c in coins], y=volume_values)])
fig3.update_layout(
    title="24h Trading Volume Comparison (All 8 Coins)",
    xaxis_title="Cryptocurrency",
    yaxis_title="24h Volume (USD)",
    template="plotly_dark",
    height=450
)

fig3.show()

# ============================================================
# TASK 5 → Explanation (for your submission)
# ============================================================

explanation = """
I used the CoinGecko API to fetch real-time cryptocurrency data.
The API provided price, 24-hour price change percentage, 24-hour trading volume,
and 7-day historical price trends for 8 cryptocurrencies.
I visualized the data using line charts and bar charts to understand market trends,
compare trading volumes, and observe price fluctuations clearly.
"""
print("\n===== PROJECT EXPLANATION =====\n")
print(explanation)