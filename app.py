from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# List of cryptocurrencies to fetch data for
cryptos = [
    'bitcoin', 'solana', 'ripple', 'pepe', 'polkadot', 'dogecoin', 
    'raydium', 'okb', 'uniswap', 'ethereum', 'tether', 'binancecoin'
]

# New route added to fix the 404 error
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Crypto API!"})  # Simple JSON response for the home route

@app.route('/crypto-data')
def crypto_data():
    try:
        # Constructing the API URL to fetch crypto prices
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            f"?ids={','.join(cryptos)}&vs_currencies=usd"
            "&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
        )

        response = requests.get(url)  # Making the request

        if response.status_code == 200:
            data = response.json()  # Parsing the response
            return jsonify(data)  # Returning the data as JSON
        else:
            return jsonify({"error": "Failed to fetch data"}), response.status_code  # Handling request failure
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500  # Handling unexpected errors

if __name__ == '__main__':
    app.run(debug=True)  # Running the Flask app
