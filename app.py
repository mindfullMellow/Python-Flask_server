import requests
from flask import Flask, jsonify

app = Flask(__name__)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Crypto API",
        "status": "Running",
        "available_route": "/crypto-data",
        "cryptos": [
            "bitcoin", "ethereum", "solana", "binancecoin", "ripple", 
            "cardano", "dogecoin", "polkadot", "matic-network", "litecoin",
            "pepe", "dogwifhat", "raydium", "okb", "uniswap", "tether"
        ]
    })

@app.route('/crypto-data')
def get_crypto_data():
    params = {
        "ids": "bitcoin,ethereum,solana,binancecoin,ripple,cardano,dogecoin,polkadot,"
               "matic-network,litecoin,pepe,dogwifhat,raydium,okb,uniswap,tether",
        "vs_currencies": "usd",
        "include_market_cap": "true",  
        "include_24hr_vol": "true",    
        "include_24hr_change": "true"
    }
    
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        raw_data = response.json()
        
        formatted_data = {}
        for crypto, details in raw_data.items():
            formatted_data[crypto] = {
                "price_id": details["usd"],
                "market_cap_id": details.get("usd_market_cap", "N/A"),
                "volume_id": details.get("usd_24h_vol", "N/A"),
                "change_24h_id": round(details.get("usd_24h_change", 0), 2)
            }
        
        return jsonify(formatted_data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
