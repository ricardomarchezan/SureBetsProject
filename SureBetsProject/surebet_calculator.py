# surebet_calculator.py
# This module contains the core logic for identifying the best odds within a market
# and calculating the profit margin to determine if a surebet exists.

from models import Game, Market, Odd

def find_best_odds(market: Market) -> tuple[Odd | None, Odd | None]:
    """
    Finds the highest available odds for each side of a 2-way market.
    For example, in a 'totals' market, it finds the best 'Over' odd and the best 'Under' odd.

    Args:
        market: A Market object containing a list of outcomes.

    Returns:
        A tuple containing the best Odd object for each side (best_odd_A, best_odd_B),
        or (None, None) if the market is not a clear 2-way market.
    """
    best_outcome_A = None
    best_outcome_B = None

    # Identify the two unique outcome names in the market (e.g., ["Over", "Under"] or ["Team A", "Team B"]).
    outcome_names = list(set(o.name for o in market.outcomes))
    
    # A surebet can only be calculated for markets with exactly two opposing outcomes.
    if len(outcome_names) != 2:
        return None, None 

    name_A, name_B = outcome_names[0], outcome_names[1]

    # Iterate through all odds in the market to find the highest price for each outcome.
    for odd in market.outcomes:
        if odd.name == name_A:
            # If this is the first odd for outcome A or its price is higher than the current best, update it.
            if best_outcome_A is None or odd.price > best_outcome_A.price:
                best_outcome_A = odd
        elif odd.name == name_B:
            # If this is the first odd for outcome B or its price is higher than the current best, update it.
            if best_outcome_B is None or odd.price > best_outcome_B.price:
                best_outcome_B = odd
    
    return best_outcome_A, best_outcome_B

def find_surebets_for_game(game: Game) -> list:
    """
    Analyzes all markets within a single game and returns a list of any surebets found.

    Args:
        game: A Game object containing all its markets.

    Returns:
        A list of dictionaries, where each dictionary contains detailed information
        about a found surebet. Returns an empty list if no surebets are found.
    """
    surebets_found = []

    # Check each market (e.g., 'totals 2.5', 'h2h') within the game.
    for market in game.markets.values():
        best_odd_A, best_odd_B = find_best_odds(market)

        # Proceed only if we found the best odds for both sides of the market.
        if best_odd_A and best_odd_B:
            # The core surebet formula: calculate the sum of the inverse of the odds.
            margin = (1 / best_odd_A.price) + (1 / best_odd_B.price)

            # If the margin is less than 1, it's a guaranteed profit (a surebet).
            if margin < 1:
                # Calculate the profit percentage.
                profit = (1 - margin) * 100
                
                # A surebet is found! Store all relevant information in a dictionary.
                surebet_info = {
                    "game": game,
                    "market": market,
                    "best_odd_A": best_odd_A,
                    "best_odd_B": best_odd_B,
                    "profit_margin": profit
                }
                surebets_found.append(surebet_info)

    return surebets_found
