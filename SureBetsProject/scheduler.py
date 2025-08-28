# scheduler.py
# This script is the main entry point for running the bot.
# It can either run the check once (manual mode) or run it repeatedly
# on a schedule (automated mode), based on the settings in config.py.

import time
import config
from main import run_single_check  # Imports the main function that performs the check.

def start_scheduler():
    """Starts the main automation loop."""
    
    print("--- AUTOMATION MODE STARTED ---")
    print(f"Checking for surebets every {config.RUN_INTERVAL_MINUTES} minutes.")
    print("Press Ctrl+C to stop the bot at any time.")
    
    while True:
        try:
            print("\n=======================================================")
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting new check cycle...")
            
            # Call the main function that does all the work.
            run_single_check()
            
            print(f"Check finished. Next check in {config.RUN_INTERVAL_MINUTES} minutes.")
            print("=======================================================\n")
            
            # Wait for the defined interval before the next run.
            time.sleep(config.RUN_INTERVAL_MINUTES * 60)
            
        except KeyboardInterrupt:
            # Allows the user to stop the bot cleanly using Ctrl+C.
            print("\n\n--- AUTOMATION STOPPED BY USER ---")
            break
        except Exception as e:
            # Catches any other unexpected error to prevent the loop from crashing.
            print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")
            print("Waiting for the next cycle to try again...")
            time.sleep(config.RUN_INTERVAL_MINUTES * 60)


# This is the main entry point when the script is executed.
if __name__ == "__main__":
    # Check the flag in the config file to decide which mode to run.
    if config.AUTOMATION_ENABLED:
        # If automation is on, start the continuous scheduler.
        start_scheduler()
    else:
        # If automation is off, run the check only once and then exit.
        print("--- MANUAL RUN MODE ---")
        print("Automation is disabled in config.py. Running a single check.")
        run_single_check()
        print("\n--- MANUAL RUN FINISHED ---")
