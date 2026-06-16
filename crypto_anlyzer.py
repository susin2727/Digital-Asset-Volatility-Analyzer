# ===========================================
# Crypto Volatility & Risk Analyzer (Simple)
# ===========================================

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Download Bitcoin Data (1 year)
btc = yf.Ticker("BTC-USD")
data = btc.history(period="1y")

# Save raw data
data.to_csv("crypto_prices.csv")

print("=== First 5 rows of data ===")
print(data.head())

# 2. Calculate Daily Returns
data['Return'] = data['Close'].pct_change()

# 3. Calculate Volatility
daily_volatility = data['Return'].std()
annual_volatility = daily_volatility * np.sqrt(252)

print(f"\nDaily Volatility: {daily_volatility:.4f}")
print(f"Annual Volatility: {annual_volatility:.4f}")

# 4. Value at Risk (VaR)
confidence_level = 0.05
VaR = data['Return'].quantile(confidence_level)

print(f"\nValue at Risk (5% level): {VaR:.4f}")

# 5. Visualizations
# 1) Price Trend
plt.figure(figsize=(12,6))
plt.plot(data.index, data['Close'], label='Close Price')
plt.title('Crypto Price Trend')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.savefig("price_trend.png")   # <-- SAVES IMAGE
plt.show()

# 2) Return Distribution
plt.figure(figsize=(12,6))
sns.histplot(data['Return'].dropna(), bins=50, kde=True)
plt.title('Return Distribution')
plt.xlabel('Daily Return')
plt.savefig("return_distribution.png")   # <-- SAVES IMAGE
plt.show()

# 3) Cumulative Returns
plt.figure(figsize=(12,6))
data['Return'].dropna().cumsum().plot()
plt.title('Cumulative Returns')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.savefig("cumulative_returns.png")   # <-- SAVES IMAGE
plt.show()

# 6. Save processed data
data.to_csv("crypto_analysis_results.csv")

print("\nAnalysis complete! Files saved:")
print("1. crypto_prices.csv")
print("2. crypto_analysis_results.csv")