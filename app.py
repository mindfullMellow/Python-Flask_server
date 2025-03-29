import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# List of cryptocurrencies to fetch data for
cryptos = [
    'bitcoin', 'solana', 'ripple', 'pepe', 'polkadot', 'dogecoin', 
    'raydium', 'okb', 'uniswap', 'ethereum', 'tether', 'binancecoin'
]

# Home route to prevent 404 error
@app.route('/')
def home():
    return "Welcome to the Flask API!"

# Route to fetch crypto data
@app.route('/crypto-data')
def crypto_data():
    try:
        # Get API key from environment variables
        api_key = os.environ.get("KEY")

        if not api_key:
            return jsonify({"error": "API key is missing"}), 500

        # CoinGecko API URL with API key
        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={','.join(cryptos)}&vs_currencies=usd"
            "&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
            f"&x_cg_pro_api_key={api_key}"
        )

        response = requests.get(url)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
