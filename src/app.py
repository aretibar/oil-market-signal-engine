import pandas as pd
import matplotlib.pyplot as plt

# Make pandas output easier to read in PyCharm
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", None)

# Load data
inventory = pd.read_csv("../data/inventory.csv", skiprows=4)
production = pd.read_csv("../data/production.csv", skiprows=4)
prices = pd.read_csv("../data/oil_prices.csv", skiprows=4)

# Clean column names
inventory.columns = ["Date", "Inventory"]
production.columns = ["Date", "Production"]
prices.columns = ["Date", "Price"]

# Convert dates
inventory["Date"] = pd.to_datetime(inventory["Date"])
production["Date"] = pd.to_datetime(production["Date"])
prices["Date"] = pd.to_datetime(prices["Date"])

# Quick inspection
print("=" * 60)
print("RAW DATA INSPECTION")
print("=" * 60)

for name, frame in [("Inventory", inventory), ("Production", production), ("Prices", prices)]:
    print(f"\n--- {name} ---")
    print("Shape:", frame.shape)
    print("Columns:")
    for col in frame.columns:
        print(" -", col)
    print("Date range:", frame["Date"].min().date(), "to", frame["Date"].max().date())
    print(frame.head(3))
    print()

# Merge datasets
df = inventory.merge(production, on="Date", how="inner")
df = df.merge(prices, on="Date", how="inner")
df = df.sort_values(by="Date")

# Feature engineering
df["Inventory_Change"] = df["Inventory"].pct_change() * 100
df["Production_Change"] = df["Production"].pct_change() * 100
df["Price_MA_30"] = df["Price"].rolling(window=30).mean()

# Remove rows with NaN values
df = df.dropna()

print("=" * 60)
print("MERGED DATAFRAME INSPECTION")
print("=" * 60)
print("Shape:", df.shape)
print("Columns:")
for col in df.columns:
    print(" -", col)
print("Date range:", df["Date"].min().date(), "to", df["Date"].max().date())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

# Signal function
def get_signal(row):
    inv = row["Inventory_Change"]
    prod = row["Production_Change"]

    if inv < -2 and prod < 0:
        return "STRONG BULLISH"
    elif inv > 2 and prod > 0:
        return "STRONG BEARISH"
    elif inv < -2:
        return "BULLISH"
    elif inv > 2:
        return "BEARISH"
    else:
        return "NEUTRAL"

# Confidence function
def get_confidence(row):
    score = abs(row["Inventory_Change"]) + abs(row["Production_Change"])

    if score > 5:
        return "HIGH"
    elif score > 2:
        return "MEDIUM"
    else:
        return "LOW"

# Apply logic
df["Signal"] = df.apply(get_signal, axis=1)
df["Confidence"] = df.apply(get_confidence, axis=1)

# Latest market analysis
latest = df.iloc[-1]
trend = "UPTREND" if latest["Price"] > latest["Price_MA_30"] else "DOWNTREND"

print("\n" + "=" * 60)
print("MARKET ANALYSIS")
print("=" * 60)
print("Date:", latest["Date"].date())
print("Signal:", latest["Signal"])
print("Confidence:", latest["Confidence"])
print(f"Inventory Change: {latest['Inventory_Change']:.2f}%")
print(f"Production Change: {latest['Production_Change']:.2f}%")
print("Trend:", trend)

explanations = {
    "STRONG BULLISH": "Supply is tightening (inventory down and production down). Potential upward pressure on prices.",
    "STRONG BEARISH": "Supply is increasing (inventory up and production up). Potential downward pressure on prices.",
    "BULLISH": "Inventory decline suggests tightening supply.",
    "BEARISH": "Inventory build suggests oversupply.",
    "NEUTRAL": "Market conditions are neutral."
}
print("Explanation:", explanations[latest["Signal"]])

print("\nLATEST 10 ROWS")
print(df[["Date", "Inventory", "Production", "Price", "Inventory_Change", "Production_Change", "Signal", "Confidence"]].tail(10))

# Plot 1
plt.figure(figsize=(12, 5))
plt.plot(df["Date"], df["Price"])
plt.title("Oil Price vs Time")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True, alpha=0.3)
plt.show()

# Plot 2
plt.figure(figsize=(12, 5))
plt.plot(df["Date"], df["Price"], label="Price")
plt.plot(df["Date"], df["Price_MA_30"], label="30-day MA")
plt.title("Oil Price with 30-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()