from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

cryptos = [
    'bitcoin', 'solana', 'ripple', 'pepe', 'polkadot', 'dogecoin', 
    'raydium', 'okb', 'uniswap', 'ethereum', 'tether', 'binancecoin'
]

@app.route('/crypto-data')
def crypto_data():
    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            f"?ids={','.join(cryptos)}&vs_currencies=usd"
            "&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
        )

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": "Failed to fetch data"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
