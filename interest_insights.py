# Interest Rate Analyzer & Investment Shift Recommender (Real-Time Web App)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Pakistan Interest Rate Insights", layout="wide")
st.title("🇵🇰 Pakistan Interest Rate & Mutual Fund Strategy Tool")

# --------------------------- Fetch Real-Time Interest Rate from SBP ---------------------------
@st.cache_data(ttl=86400)
def fetch_interest_rate():
    try:
        url = "https://www.sbp.org.pk"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rate_section = soup.find(text="Policy Rate")
        if rate_section:
            parent = rate_section.find_parent('tr')
            rate_value = parent.find_all('td')[1].text.strip()
            rate = float(rate_value.replace('%', ''))
            return {'current_rate': rate, 'last_updated': dt.date.today().strftime('%Y-%m-%d')}
    except:
        pass
    return {'current_rate': 8.5, 'last_updated': '2025-07-01'}  # fallback

# --------------------------- Simulated Forecast (Placeholder) ------------------------
def forecast_interest_rate(current_rate):
    return current_rate - 1.0  # Replace with real model (ARIMA, Prophet, etc.)

# --------------------------- Dummy Fund Performance Data -----------------------------
def load_fund_data():
    dates = pd.date_range(start='2002-01-01', periods=24, freq='Q')
    df = pd.DataFrame({
        'Date': dates,
        'StockFundReturn': [10, 8, -12, -6, 2, 5, 6, 12, 18, 25, 30, 28,
                            20, 18, 15, 13, 12, 10, 9, 10, 11, 12, 14, 16],
        'LowRiskFundReturn': [12, 11, 9, 7, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10,
                              9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 6.5, 6.0, 6.0, 6.2, 6.5, 7.0],
        'InterestRate': [13.25, 12.5, 9.0, 7.0, 7.0, 7.25, 8.0, 9.5, 10.75, 13.75, 15.0, 17.0,
                         17.0, 16.0, 15.25, 14.0, 13.5, 13.0, 12.5, 12.0, 11.0, 10.0, 9.0, 8.5]
    })
    return df

# --------------------------- Recommendation Engine -----------------------------------
def recommend_shift(current_rate, forecast_rate):
    if forecast_rate < current_rate - 1.5:
        return "🔼 Shift to high-risk equity funds (stocks, equity mutual funds)"
    elif forecast_rate > current_rate + 1.0:
        return "🔽 Stay in low-risk funds (money market, income funds)"
    else:
        return "⚖️ Maintain a balanced fund strategy"

# --------------------------- Streamlit Dashboard -------------------------------------
rate_data = fetch_interest_rate()
current_rate = rate_data['current_rate']
forecast_rate = forecast_interest_rate(current_rate)

st.subheader(f"🏦 Current SBP Interest Rate: {current_rate}% (as of {rate_data['last_updated']})")
st.subheader(f"📈 Forecasted Rate: {forecast_rate}%")

st.markdown("### Investment Strategy Recommendation")
st.success(recommend_shift(current_rate, forecast_rate))

fund_df = load_fund_data()
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(fund_df['Date'], fund_df['InterestRate'], color='red', label='SBP Rate', linewidth=2)
ax1.set_ylabel('Interest Rate (%)', color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.plot(fund_df['Date'], fund_df['StockFundReturn'], label='Stock Fund Return', linestyle='--', color='green')
ax2.plot(fund_df['Date'], fund_df['LowRiskFundReturn'], label='Low-Risk Fund Return', linestyle='--', color='blue')
ax2.set_ylabel('Fund Return (%)')

fig.tight_layout()
fig.suptitle('Interest Rate vs Fund Performance in Pakistan', fontsize=16)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
st.pyplot(fig)

st.markdown("---")
st.markdown("🔁 *Interest rate data is fetched from SBP.gov.pk. Forecasting model is placeholder and can be replaced with Prophet, ARIMA, etc.*")

