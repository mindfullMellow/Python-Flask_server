import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

COINGECKO_API_KEY = "CG-75vCP2UBBY936h9FgAAtfNKQ"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Crypto API"})

@app.route('/crypto-data')
def get_crypto_data():
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "x_cg_pro_api_key": COINGECKO_API_KEY  # Free API users should remove this line
    }
    
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
