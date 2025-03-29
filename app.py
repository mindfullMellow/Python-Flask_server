import requests
from flask import Flask, jsonify

app = Flask(__name__)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

@app.route('/')
def home():
    debug_info = {
        "status": "Service is running",
        "api_url": COINGECKO_API_URL,
        "expected_endpoint": "/crypto-data",
    }
    return jsonify(debug_info)

@app.route('/crypto-data')
def get_crypto_data():
    params = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "usd"
    }
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
