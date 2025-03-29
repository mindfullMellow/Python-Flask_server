import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Crypto API"})

@app.route('/crypto-data')
def get_crypto_data():
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,  # Fetches top 250 coins
        "page": 1,
        "sparkline": False
    }
    
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        data = response.json()
        
        # Filter only needed data
        filtered_data = [
            {
                "id": coin["id"],
                "symbol": coin["symbol"],
                "price": coin["current_price"],
                "market_cap": coin["market_cap"],
                "volume": coin["total_volume"],
                "change_24h": coin["price_change_percentage_24h"]
            }
            for coin in data
        ]
        
        return jsonify(filtered_data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
