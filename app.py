import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Crypto API"})

@app.route('/crypto-data')
def get_crypto_data():
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }
    
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        data = response.json()
        
        print("Full API Response:", data)  # Debugging log
        
        if not isinstance(data, list):  # If API response is not a list, return error
            return jsonify({"error": "Unexpected API response format", "response": data})

        filtered_data = {
            coin.get("id"): {
                "usd": coin.get("current_price"),
                "usd_market_cap": coin.get("market_cap"),
                "usd_24h_vol": coin.get("total_volume"),
                "usd_24h_change": coin.get("price_change_percentage_24h")
            }
            for coin in data if coin.get("id")  # Avoids processing invalid data
        }
        
        return jsonify(filtered_data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)})

if __name__ == '__main__':
    app.run(debug=True)