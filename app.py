import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# List of cryptocurrencies to fetch
cryptos = [
    'bitcoin', 'solana', 'ripple', 'pepe', 'polkadot', 'dogecoin',
    'raydium', 'okb', 'uniswap', 'ethereum', 'tether', 'binancecoin'
]

# Get API key from environment variable
API_KEY = os.getenv("KEY")

@app.route('/crypto-data')
def crypto_data():
    try:
        # Construct the API URL with the API key
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            f"?ids={','.join(cryptos)}&vs_currencies=usd"
            "&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
            f"&x_cg_api_key={API_KEY}"
        )

        response = requests.get(url)

        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 429:
            return jsonify({"error": "Rate limit exceeded. Try again later."}), 429
        else:
            return jsonify({"error": "Failed to fetch data"}), response.status_code

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
