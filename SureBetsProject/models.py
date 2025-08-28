# models.py
# This file defines the data structures (classes) used to represent games,
# markets, and odds in a structured way.

class Odd:
    """Represents a single betting odd from a specific bookmaker for one outcome."""
    def __init__(self, name: str, price: float, bookmaker: str, point: float = None):
        self.name = name          # The name of the outcome (e.g., 'Home', 'Away', 'Over').
        self.price = price        # The decimal betting odd (e.g., 1.95).
        self.bookmaker = bookmaker# The key of the bookmaker offering the odd (e.g., 'betfair').
        self.point = point        # The point value for totals or spreads (e.g., 2.5 for Over/Under).

    def __repr__(self):
        """Provides a string representation for debugging."""
        return f"Outcome: {self.name:<18} | Odd: {self.price:<6} | Bookmaker: {self.bookmaker}"

class Market:
    """Represents a specific betting market within a game, like 'totals' at a 2.5 line."""
    def __init__(self, key: str, point: float):
        self.key = key          # The type of market (e.g., 'h2h', 'totals', 'spreads').
        self.point = point      # The line for this market (e.g., 2.5).
        self.outcomes = []      # A list to hold all Odd objects for this market.

    def __str__(self):
        """Provides a user-friendly, multi-line string representation of the market."""
        market_title = f"Market: {self.key.capitalize()} (Line: {self.point})"
        outcomes_list = [f"  -> {odd}" for odd in self.outcomes]
        return f"{market_title}\n" + "\n".join(outcomes_list)

    def __repr__(self):
        """Provides a concise string representation for debugging."""
        return f"Market(key='{self.key}', point={self.point}, outcomes_count={len(self.outcomes)})"

class Game:
    """Represents a single sporting event, containing all its associated markets and odds."""
    def __init__(self, id: str, home_team: str, away_team: str, commence_time: str):
        self.id = id                      # The unique ID of the game from the API.
        self.home_team = home_team
        self.away_team = away_team
        self.commence_time = commence_time # The start time of the game (in ISO 8601 format).
        self.markets = {}                 # A dictionary to store Market objects, keyed by a unique market ID.

    def __repr__(self):
        """Provides a simple string representation of the game for easy identification."""
        return f"Game: {self.home_team} vs {self.away_team} (Starts: {self.commence_time})"
