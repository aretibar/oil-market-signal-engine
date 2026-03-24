from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)


def load_data():
    # Load CSV files
    inventory = pd.read_csv("data/inventory.csv", skiprows=4)
    production = pd.read_csv("data/production.csv", skiprows=4)
    prices = pd.read_csv("data/oil_prices.csv", skiprows=4)

    # Rename columns
    inventory.columns = ["Date", "Inventory"]
    production.columns = ["Date", "Production"]
    prices.columns = ["Date", "Price"]

    # Convert dates
    inventory["Date"] = pd.to_datetime(inventory["Date"])
    production["Date"] = pd.to_datetime(production["Date"])
    prices["Date"] = pd.to_datetime(prices["Date"])

    # Merge datasets
    df = inventory.merge(production, on="Date", how="inner")
    df = df.merge(prices, on="Date", how="inner")

    # Sort by date
    df = df.sort_values(by="Date").reset_index(drop=True)

    return df


@app.route("/")
def home():
    return jsonify({"message": "Oil Market Signal API is running"})


@app.route("/data")
def get_data():
    df = load_data()
    latest_rows = df.tail(5).copy()
    latest_rows["Date"] = latest_rows["Date"].astype(str)
    return jsonify(latest_rows.to_dict(orient="records"))


@app.route("/latest-price")
def latest_price():
    df = load_data()
    latest = df.iloc[-1]

    return jsonify({
        "date": str(latest["Date"].date()),
        "price": float(latest["Price"])
    })


@app.route("/signal")
def get_signal():
    df = load_data()

    # Calculate changes
    df["inventory_change"] = df["Inventory"].diff()
    df["price_change"] = df["Price"].diff()

    latest = df.iloc[-1]

    # Use the latest 4 changes to create a trend signal
    inventory_trend = df["inventory_change"].tail(4).mean()
    price_trend = df["price_change"].tail(4).mean()

    # Handle missing values safely
    if pd.isna(inventory_trend):
        inventory_trend = 0.0

    if pd.isna(price_trend):
        price_trend = 0.0

    # Signal logic
    if inventory_trend < 0 and price_trend > 0:
        signal = "Strong Bullish"
    elif inventory_trend > 0 and price_trend < 0:
        signal = "Strong Bearish"
    elif price_trend > 0:
        signal = "Bullish"
    elif price_trend < 0:
        signal = "Bearish"
    else:
        signal = "Neutral"

    return jsonify({
        "date": str(latest["Date"].date()),
        "inventory_trend": float(inventory_trend),
        "price_trend": float(price_trend),
        "signal": signal
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)