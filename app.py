import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS to handle cross-origin requests

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes (prevents browser blocking requests due to security policies)
CORS(app)

# CoinGecko API endpoint for fetching cryptocurrency data
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"

# Home route to check if the server is running
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Crypto API"})

# Route to fetch cryptocurrency data
@app.route('/crypto-data')
def get_crypto_data():
    # Define query parameters for CoinGecko API request
    params = {
        "vs_currency": "usd",  # Get prices in USD
        "order": "market_cap_desc",  # Sort by highest market cap
        "per_page": 250,  # Max number of coins per request
        "page": 1,  # Fetch the first page
        "sparkline": False  # Disable sparkline data (mini charts)
    }
    
    try:
        # Make a request to the CoinGecko API
        response = requests.get(COINGECKO_API_URL, params=params)
        data = response.json()  # Convert response to JSON format
        
        # Check if API returned an expected list of coins
        if not isinstance(data, list):  
            return jsonify({"error": "Unexpected API response format"})

        # Process and filter the needed data for each coin
        filtered_data = {
            coin["id"]: {  # Use coin ID as the key
                "usd": coin["current_price"],  # Current price in USD
                "usd_market_cap": coin["market_cap"],  # Market capitalization
                "usd_24h_vol": coin["total_volume"],  # 24-hour trading volume
                "usd_24h_change": coin["price_change_percentage_24h"]  # 24-hour price change
            }
            for coin in data  # Loop through each coin from the API response
        }
        
        return jsonify(filtered_data)  # Return the filtered data as JSON
    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({"error": "Failed to fetch data", "details": str(e)})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for easier troubleshooting
