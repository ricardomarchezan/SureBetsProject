# test_runner.py
# This script runs a unit test to verify that the core components of the bot
# are working as expected. It tests both the surebet calculation logic and
# the Telegram notification system.

from models import Game, Market, Odd
from surebet_calculator import find_surebets_for_game
from notifier import send_telegram_alert # Import the notifier module to test it.

def run_surebet_test():
    """
    Executes a quality control test, which includes creating a mock surebet,
    detecting it, and sending a notification.
    """
    
    print("--- STARTING QUALITY CONTROL TEST (WITH NOTIFICATION) ---")
    print("Creating a mock 'trap game' with a guaranteed surebet...")

    # 1. Manually create a fake Game object.
    # This game contains a guaranteed surebet opportunity by using two odds of 2.1.
    # The formula (1 / 2.1) + (1 / 2.1) results in a value less than 1, which is a surebet.
    test_game = Game(id="test_game_01", home_team="Test Team A", away_team="Test Team B", commence_time="2099-01-01T12:00:00Z")
    test_market = Market(key="totals", point=2.5)
    
    # The odds that create the surebet.
    surebet_odd_over = Odd(name="Over", price=2.1, bookmaker="TestBookie_A", point=2.5)
    surebet_odd_under = Odd(name="Under", price=2.1, bookmaker="TestBookie_B", point=2.5)
    
    # Normal odds that should be ignored by the calculator.
    normal_odd_over = Odd(name="Over", price=1.9, bookmaker="NormalBookie_C", point=2.5)
    normal_odd_under = Odd(name="Under", price=1.9, bookmaker="NormalBookie_D", point=2.5)
    
    test_market.outcomes.extend([surebet_odd_over, surebet_odd_under, normal_odd_over, normal_odd_under])
    test_game.markets['totals_2.5'] = test_market

    print("Mock game created. Feeding it to the 'surebet_calculator'...")
    
    # 2. Pass the fake game to the calculation engine.
    found_surebets = find_surebets_for_game(test_game)

    print("\n--- TEST RESULT ---")
    
    # 3. Check if the calculation logic successfully found the surebet.
    if found_surebets:
        print("\n✅ PASS! The bot's brain correctly detected the surebet.")
        
        surebet = found_surebets[0]
        profit_margin = surebet['profit_margin']
        game_info = surebet['game']
        market_info = surebet['market']
        odd_A = surebet['best_odd_A']
        odd_B = surebet['best_odd_B']

        # 4. Format the Telegram message exactly as the main bot would.
        message = (
            f"<b>💰 TEST SUREBET FOUND! 💰</b>\n\n"
            f"<b>Guaranteed Profit:</b> {profit_margin:.2f}%\n\n"
            f"<b>Game:</b> {game_info.home_team} vs {game_info.away_team}\n"
            f"<b>Market:</b> {market_info.key.capitalize()} (Line: {market_info.point})\n\n"
            f"<b>Bets to place:</b>\n"
            f"  1. <b>{odd_A.price}</b> on <code>{odd_A.name}</code> at <b>{odd_A.bookmaker}</b>\n"
            f"  2. <b>{odd_B.price}</b> on <code>{odd_B.name}</code> at <b>{odd_B.bookmaker}</b>"
        )
        
        print("\nFormatting and sending test alert to Telegram...")
        # 5. Call the notification function to test the Telegram integration.
        send_telegram_alert(message)
        
    else:
        print("\n❌ FAIL! The bot's brain DID NOT detect the guaranteed surebet.")

# This is the entry point for running the test script directly.
if __name__ == "__main__":
    run_surebet_test()
