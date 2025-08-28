# notifier.py
# This module handles sending formatted alert messages to a Telegram chat.

import requests
import config 

def send_telegram_alert(message: str):
    """
    Sends a message to the configured Telegram chat.
    It checks the config file to ensure notifications are enabled and credentials are set.

    Args:
        message: The string message to be sent. HTML formatting is supported.
    """
    
    # If Telegram notifications are globally disabled in config.py, do nothing.
    if not config.TELEGRAM_ENABLED:
        print("Telegram notifications are disabled. Skipping alert.")
        return 

    # Validate that the bot token and chat ID are properly configured.
    if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == 'SEU_TOKEN_AQUI':
        print("WARNING: Telegram Bot Token is not set in config.py. Cannot send alert.")
        return
    if not config.TELEGRAM_CHAT_ID or config.TELEGRAM_CHAT_ID == 'SEU_CHAT_ID_AQUI':
        print("WARNING: Telegram Chat ID is not set in config.py. Cannot send alert.")
        return

    # The URL for the Telegram Bot API's sendMessage method.
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"

    # The payload containing the recipient's chat ID and the message text.
    # 'parse_mode': 'HTML' allows for rich formatting like <b>bold</b> and <code>code</code>.
    payload = {
        'chat_id': config.TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        # Send the message via an HTTP POST request.
        response = requests.post(url, json=payload)
        
        # Raise an exception for HTTP errors (e.g., 401 for an invalid token).
        response.raise_for_status() 
        
        # Check the 'ok' field in Telegram's JSON response to confirm the message was sent.
        if response.json().get('ok'):
            print("Surebet alert sent successfully to Telegram!")
        else:
            print(f"Failed to send Telegram alert: {response.text}")

    # Catch any network-related errors during the request.
    except requests.exceptions.RequestException as e:
        print(f"Connection error while trying to send Telegram alert: {e}")

