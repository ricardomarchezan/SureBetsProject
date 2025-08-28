# descobrir_esportes.py
# This script fetches and displays a list of all available sports from The Odds API.
# It helps in finding the correct 'sport_key' to use in the main config.py file.

import requests
import json

# IMPORTANT: Paste your API key from The Odds API here to run this script.
API_KEY = ''

# The API endpoint for retrieving the list of sports.
url = 'https://api.the-odds-api.com/v4/sports'

# Set the required parameters for the API request.
params = {
    'api_key': API_KEY
}

print("Fetching the list of all available sports from the API...")

try:
    # Send the GET request to the API.
    response = requests.get(url, params=params)
    
    # Check if the request was successful (raises an error for 4xx or 5xx responses).
    response.raise_for_status()  

    # Parse the JSON data from the response.
    sports_list = response.json()

    print("\nSUCCESS! List of sports received.")
    print("-----------------------------------------")
    
    # Pretty-print the JSON list for better readability.
    print(json.dumps(sports_list, indent=4))
    print("-----------------------------------------")

# Handle potential HTTP errors, like an invalid API key or bad request.
except requests.exceptions.HTTPError as err:
    print(f"\nHTTP Error while fetching data: {err}")
    print(f"Response body: {err.response.text}") # The response body often contains useful debug info.

# Handle other network-related errors, like a connection failure.
except requests.exceptions.RequestException as e:
    print(f"\nA connection error occurred: {e}")
