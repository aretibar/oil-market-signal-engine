# Oil Market Signal Engine

A backend-style data project that analyzes oil market fundamentals (inventory, production, prices) and exposes insights through an API.

---

## 📊 Overview

This project simulates how energy analysts monitor supply-demand dynamics in the oil market using real-world datasets.

It processes multiple data sources and generates simple market signals.

---

## ⚙️ Features

- Data cleaning and merging from multiple sources
- Time-series analysis of oil fundamentals
- REST API for accessing data
- Market signal generation (Bullish / Bearish / Neutral)

---

## 🔌 API Endpoints

- `/` → API status check  
- `/data` → latest oil market records  
- `/signal` → market signal based on recent changes  

---

## Live API
https://oil-market-signal-engine.onrender.com

--- 

### Endpoints
- `/`
- `/data`
- `/latest-price`
- `/signal`

---

## 🛠️ Tech Stack

- Python
- Pandas
- Flask
- Matplotlib

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python src/api.py