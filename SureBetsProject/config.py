# config.py

# --- API ---
API_KEY = ''  # Your key from The Odds API.
TARGET_SPORTS = [
    'soccer_brazil_serie_b', 'soccer_conmebol_copa_libertadores'
]  # Sports to scan for odds.
TARGET_MARKETS = 'totals,spreads'  # Bet markets to fetch (h2h, totals, spreads).
REGIONS = 'eu,uk,us,br,au'  # Bookmaker regions to check.
ODDS_FORMAT = 'decimal'  # 'decimal' or 'american' odds format.

# --- Telegram ---
TELEGRAM_ENABLED = True  # Enable or disable Telegram notifications.
TELEGRAM_BOT_TOKEN = ''  # Your Telegram bot's token.
TELEGRAM_CHAT_ID = ''  # The chat ID to send alerts to.

# --- Automation ---
AUTOMATION_ENABLED = True  # Set to True to run scans automatically.
RUN_INTERVAL_MINUTES = 60  # Minutes between scans when automation is enabled.
