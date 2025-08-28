# main.py
# This is the main engine of the bot. It contains the core logic to:
# 1. Fetch odds data from the API.
# 2. Process and structure the data into objects.
# 3. Analyze the data to find surebet opportunities.
# 4. Trigger notifications for any surebets found.

import requests
import time
import config
from models import Game, Market, Odd
from surebet_calculator import find_surebets_for_game
from notifier import send_telegram_alert

def process_api_data(api_data: list) -> list[Game]:
    """
    Transforms the raw list of data from the API into a structured list of Game objects.
    It groups all bookmaker odds by game, and then by market.

    Args:
        api_data: The raw JSON list response from The Odds API.

    Returns:
        A list of Game objects, each containing structured market and odds data.
    """
    processed_games = {}  # Use a dict to efficiently group odds by game ID.
    
    for game_data in api_data:
        game_id = game_data['id']
        
        # If this is the first time we see this game, create a new Game object.
        if game_id not in processed_games:
            processed_games[game_id] = Game(
                id=game_id, 
                home_team=game_data['home_team'], 
                away_team=game_data['away_team'], 
                commence_time=game_data['commence_time']
            )
        
        game = processed_games[game_id]
        
        # Iterate through bookmakers and their markets for the current game.
        for bookmaker in game_data['bookmakers']:
            bookmaker_key = bookmaker['key']
            for market in bookmaker['markets']:
                market_key = market['key']
                for outcome in market['outcomes']:
                    # For totals/spreads, the 'point' is the line (e.g., 2.5). Default to 0.0 for h2h.
                    point = outcome.get('point', 0.0)
                    
                    # Create a unique market ID combining the key and the line (e.g., 'totals_2.5').
                    market_id = f"{market_key}_{abs(point)}"
                    
                    # If this market doesn't exist for the game yet, create it.
                    if market_id not in game.markets:
                        game.markets[market_id] = Market(key=market_key, point=abs(point))
                    
                    # Create the Odd object and add it to the correct market.
                    odd = Odd(name=outcome['name'], price=outcome['price'], bookmaker=bookmaker_key, point=point)
                    game.markets[market_id].outcomes.append(odd)
                    
    return list(processed_games.values()) # Return the structured Game objects as a list.

def fetch_odds_for_sport(sport_key: str) -> list[Game]:
    """
    Fetches and processes odds for a single sport from The Odds API.

    Args:
        sport_key: The key for the sport to fetch (e.g., 'soccer_brazil_serie_a').

    Returns:
        A list of processed Game objects for the sport, or an empty list if an error occurs.
    """
    print(f"\n--- Fetching and processing data for: '{sport_key}' ---")
    url = f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds'
    params = {
        'api_key': config.API_KEY, 
        'regions': config.REGIONS, 
        'markets': config.TARGET_MARKETS, 
        'oddsFormat': config.ODDS_FORMAT
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx).
        
        api_data = response.json()
        if not api_data:
            print(f"No upcoming games found for '{sport_key}'.")
            return []
            
        # Process the raw data into structured objects.
        structured_games = process_api_data(api_data)
        
        print(f"SUCCESS! {len(structured_games)} games analyzed.")
        remaining_requests = response.headers.get('x-requests-remaining', 'N/A')
        print(f"API requests remaining this month: {remaining_requests}")
        
        return structured_games
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
        return []

def run_single_check():
    """
    Executes one full cycle of the bot: fetches odds for all target sports,
    analyzes them for surebets, and sends alerts for any opportunities found.
    """
    print("Starting check cycle...")
    
    # Critical check to ensure the user has configured the API key.
    if not config.API_KEY or config.API_KEY == 'SUA_CHAVE_API_AQUI':
        print("\nCRITICAL ERROR: Please set your API_KEY in the config.py file.")
        return

    all_surebets = []
    # Loop through each sport defined in the config file.
    for sport in config.TARGET_SPORTS:
        processed_games = fetch_odds_for_sport(sport)
        # For each game, run the surebet calculation logic.
        for game in processed_games:
            surebets_in_game = find_surebets_for_game(game)
            if surebets_in_game:
                all_surebets.extend(surebets_in_game)

    if not all_surebets:
        print("\nNo surebets found in this check.")
    else:
        print(f"\nSUCCESS! {len(all_surebets)} SUREBET OPPORTUNITY(S) FOUND!")
        # For each surebet found, format and send a Telegram alert.
        for surebet in all_surebets:
            message = (
                f"<b>💰 NEW SUREBET FOUND! 💰</b>\n\n"
                f"<b>Guaranteed Profit:</b> {surebet['profit_margin']:.2f}%\n\n"
                f"<b>Game:</b> {surebet['game'].home_team} vs {surebet['game'].away_team}\n"
                f"<b>Market:</b> {surebet['market'].key.capitalize()} (Line: {surebet['market'].point})\n\n"
                f"<b>Bets to place:</b>\n"
                f"  1. <b>{surebet['best_odd_A'].price}</b> on <code>{surebet['best_odd_A'].name}</code> at <b>{surebet['best_odd_A'].bookmaker}</b>\n"
                f"  2. <b>{surebet['best_odd_B'].price}</b> on <code>{surebet['best_odd_B'].name}</code> at <b>{surebet['best_odd_B'].bookmaker}</b>"
            )
            send_telegram_alert(message)

# This block allows the script to be run directly for a single check (e.g., for testing).
# The main application entry point for automation is scheduler.py.
if __name__ == "__main__":
    print("This file acts as the engine. To start automation, run scheduler.py")
    run_single_check()
