from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

def load_data():
    inventory = pd.read_csv("data/inventory.csv", skiprows=4)
    production = pd.read_csv("data/production.csv", skiprows=4)
    prices = pd.read_csv("data/oil_prices.csv", skiprows=4)

    inventory.columns = ["Date", "Inventory"]
    production.columns = ["Date", "Production"]
    prices.columns = ["Date", "Price"]

    inventory["Date"] = pd.to_datetime(inventory["Date"])
    production["Date"] = pd.to_datetime(production["Date"])
    prices["Date"] = pd.to_datetime(prices["Date"])

    df = inventory.merge(production, on="Date", how="inner")
    df = df.merge(prices, on="Date", how="inner")
    df = df.sort_values(by="Date")

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

@app.route("/signal")
def get_signal():
    df = load_data()

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    inventory_change = latest["Inventory"] - previous["Inventory"]
    production_change = latest["Production"] - previous["Production"]
    price_change = latest["Price"] - previous["Price"]

    if inventory_change < 0 and price_change > 0:
        signal = "Bullish"
    elif inventory_change > 0 and price_change < 0:
        signal = "Bearish"
    else:
        signal = "Neutral"

    return jsonify({
        "date": str(latest["Date"].date()),
        "inventory_change": float(inventory_change),
        "production_change": float(production_change),
        "price_change": float(price_change),
        "signal": signal
    })

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/latest-price")
def latest_price():
    df = load_data()
    latest = df.iloc[-1]

    return jsonify({
        "date": str(latest["Date"].date()),
        "price": float(latest["Price"])
    })