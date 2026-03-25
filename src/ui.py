import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "https://oil-market-signal-engine.onrender.com"

st.set_page_config(
    page_title="Oil Market Signal Engine",
    page_icon="📈",
    layout="wide"
)

# ---------- Custom Styling ----------
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #f8fafc;
    }
    p, div {
        color: #e2e8f0;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    .signal-box {
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("📈 Oil Market Signal Engine")
st.markdown("A backend-powered oil market dashboard built with **Flask + Pandas + Streamlit**.")

# ---------- Helper function ----------
def fetch_data(endpoint):
    url = f"{API_BASE_URL}{endpoint}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()

# ---------- Layout ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Market Overview")
    st.write(
        "This dashboard connects to the deployed API and displays oil market insights "
        "based on inventory, production, and price data."
    )

with col2:
    st.subheader("Live API")
    st.code(API_BASE_URL)

# ---------- Fetch API data ----------
try:
    signal_data = fetch_data("/signal")
    price_data = fetch_data("/latest-price")
    latest_records = fetch_data("/data")

    # Metrics row
    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Latest Date", signal_data["date"])

    with m2:
        st.metric("Latest Price", f'{price_data["price"]:.2f}')

    with m3:
        st.metric("Price Trend", f'{signal_data["price_trend"]:.2f}')

    # Signal color
    signal = signal_data["signal"]

    if "Bullish" in signal:
        bg = "#14532d"
        fg = "#dcfce7"
    elif "Bearish" in signal:
        bg = "#7f1d1d"
        fg = "#fee2e2"
    else:
        bg = "#3f3f46"
        fg = "#f4f4f5"

    st.markdown(
        f"""
        <div class="signal-box" style="background-color:{bg}; color:{fg};">
            Current Signal: {signal}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Trend details
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Inventory Trend")
        st.metric("Inventory Trend", f'{signal_data["inventory_trend"]:.2f}')

    with c2:
        st.subheader("Price Trend")
        st.metric("Price Trend", f'{signal_data["price_trend"]:.2f}')

    # Data table
    st.subheader("Latest Oil Market Records")
    df = pd.DataFrame(latest_records)
    st.dataframe(df, use_container_width=True)

except requests.exceptions.RequestException as e:
    st.error("Could not connect to the API.")
    st.exception(e)
except Exception as e:
    st.error("Something went wrong while loading the dashboard.")
    st.exception(e)