# Digital-Asset-Volatility-Analyzer

A comprehensive cryptocurrency volatility and risk analysis project with interactive dashboards.  
This project analyzes historical and live crypto price data, calculates returns, risk metrics, and visualizes insights using Python and Streamlit.

---

## 📌 Features

### 🔹 Milestone 1 – BTC Data Analysis
- Fetch 1-year BTC-USD historical price data using `yfinance`.
- Calculate daily returns and cumulative returns.
- Compute volatility and Value at Risk (VaR).
- Save raw and processed data.
- Visualizations:
  - BTC price trend
  - Return distribution
  - Cumulative returns

### 🔹 Milestone 2 – Crypto Risk Analysis Dashboard
- Multi-crypto support: BTC, ETH, SOL, ADA, DOGE, LTC, XRP, DOT.
- Calculate Sharpe ratio, beta vs BTC, rolling volatility.
- Classify risk as Low, Medium, High.
- Interactive dashboard with Plotly & Streamlit.

### 🔹 Milestone 3 – Interactive Visualization Dashboard
- Price trend and rolling volatility over time.
- Risk vs Return scatter plots.
- Radar chart for risk profile.
- KPI metrics and comparative analysis.

### 🔹 Milestone 4 – Risk Classification & Reporting
- Classify assets into risk buckets.
- Visual risk cards and distribution charts.
- Downloadable reports (CSV & PDF).
- Summary of project milestones and completion status.

---

## 📊 Dashboards and Screenshots

You can view dashboard images in the `images/` folder:

- Milestone 1: `cumulative_returns.png`, `price_trend.png`, `return_distribution.png`  
- Milestone 2: `milestone2_dashboard.png`, `milestone2p1.png`, `milestone2p2.png`  
- Milestone 3: `milestone3_dashboard.png`, `milestone3dfp.png`, `milestone3p1.png` ...  
- Milestone 4: `milestone4_dashboard.png`, `milestone4dfp.png`, `milestone4p1.png` ...

*(Refer to the `images/` folder in the repo for all screenshots.)*

---

## 🛠 Technologies Used

- Python 3.x  
- `yfinance`, `requests`  
- `pandas`, `numpy`  
- `matplotlib`, `seaborn`, `plotly`  
- `streamlit`  
- `FPDF`  

---



📌 Notes

Live data is fetched from the CoinGecko API.

Demonstrates real-time price fetching, risk metric calculation, and interactive analytics.

Exportable reports include CSV and PDF.

📁 Recommended Folder Structure
Digital-Asset-Volatility-Analyzer/
├── app.py
├── utils.py
├── crypto_analyzer.py
├── milestone_1.py
├── milestone_2_dashboard.py
├── milestone_3_dashboard.py
├── milestone_4_dashboard.py
├── data/
│   ├── crypto_prices.csv
│   ├── crypto_analysis_results.csv
│   └── crypto_metrics.csv
├── images/
│   ├── price_trend.png
│   ├── return_distribution.png
│   ├── cumulative_returns.png
│   ├── milestone2_dashboard.png
│   ├── milestone3_dashboard.png
│   └── milestone4_dashboard.png
├── requirements.txt
└── README.md
