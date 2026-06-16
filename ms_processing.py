import requests
import pandas as pd
import numpy as np
from datetime import datetime

# ===============================
# CONFIGURATION
# ===============================

coins = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "cardano": "ADA",
    "dogecoin": "DOGE"
}

DAYS = 365
BASE_URL = "https://api.coingecko.com/api/v3/coins/{}/market_chart"

# ===============================
# FETCH HISTORICAL DATA
# ===============================

price_data = {}

for coin in coins:
    url = BASE_URL.format(coin)
    params = {"vs_currency": "usd", "days": DAYS}
    data = requests.get(url, params=params).json()

    prices = pd.DataFrame(data["prices"], columns=["timestamp", coin])
    prices["Date"] = pd.to_datetime(prices["timestamp"], unit="ms")
    prices.set_index("Date", inplace=True)
    prices.drop(columns=["timestamp"], inplace=True)

    price_data[coin] = prices

# ===============================
# COMBINE DATA
# ===============================

df_prices = pd.concat(price_data.values(), axis=1)
df_prices = df_prices.dropna()
df_prices.sort_index(inplace=True)

# ===============================
# LOG RETURNS
# ===============================

df_returns = np.log(df_prices / df_prices.shift(1)).dropna()

# ===============================
# METRICS CALCULATION
# ===============================

metrics = []

btc_returns = df_returns["bitcoin"]

for coin in coins:
    returns = df_returns[coin]

    daily_vol = returns.std()
    annual_vol = daily_vol * np.sqrt(252)
    sharpe = returns.mean() / daily_vol

    if coin == "bitcoin":
        beta = 1.0
    else:
        cov = np.cov(returns, btc_returns)[0][1]
        var = np.var(btc_returns)
        beta = cov / var

    metrics.append([
        coins[coin],
        daily_vol,
        annual_vol,
        sharpe,
        beta
    ])

metrics_df = pd.DataFrame(
    metrics,
    columns=["Asset", "Daily Volatility", "Annual Volatility", "Sharpe Ratio", "Beta (vs BTC)"]
)

# ===============================
# MOVING AVERAGE & ROLLING VOL
# ===============================

for coin in coins:
    df_prices[f"{coin}_MA30"] = df_prices[coin].rolling(30).mean()
    df_returns[f"{coin}_Vol30"] = df_returns[coin].rolling(30).std()

# ===============================
# SAVE OUTPUTS
# ===============================

# Rename return columns to avoid overlap
df_returns_renamed = df_returns.add_suffix("_return")

# Combine price + returns safely
final_df = df_prices.join(df_returns_renamed)

# Save processed dataset
final_df.to_csv("data/processed_crypto_data.csv")
metrics_df.to_csv("data/crypto_metrics.csv", index = False)

print("✅ Milestone 2 data processing completed successfully")