# SureBet Arbitrage Bot

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active_development-orange.svg)

A sophisticated Python-based bot designed to identify arbitrage betting opportunities (surebets) across multiple sports and eSports in real-time. This tool automates the process of scanning, calculating, and notifying users of profitable betting scenarios.

## 🚀 Key Features

*   **Multi-Provider Architecture**: Built with a flexible, pluggable provider system. Easily integrate multiple odds APIs to maximize market coverage. Currently configured for:
    *   **TheOddsAPI** for traditional sports.
    *   **A dedicated slot for a new eSports API** (see Roadmap).
*   **Advanced Calculation Engine**: The core logic is not just a simple comparison. It intelligently handles:
    *   **2-Way Markets**: For sports like Tennis and eSports (e.g., Winner 1 vs. Winner 2).
    *   **3-Way Markets**: For sports like Soccer, correctly factoring in the Draw (Home, Draw, Away).
    *   **Complex Markets**: Differentiates between different betting lines for `Totals` (Over/Under 2.5, 3.5, etc.) and `Spreads` to avoid false positives.
*   **Real-time Telegram Alerts**: Delivers instant, beautifully formatted notifications via Telegram the moment a surebet is detected, providing all the necessary information to act quickly.
*   **Robust & Resilient**: Designed with comprehensive error handling. The bot is resilient to API downtime or unexpected data formats, ensuring continuous operation.
*   **Automated Scheduling**: Features a "set-it-and-forget-it" automated mode that runs scans at user-defined intervals.
*   **Dedicated Test Suite**: Includes a `test_runner.py` file to validate the core logic, test provider integrations, and debug API responses, ensuring system reliability.

## 💡 How It Works

The bot operates on a clean, orchestrated workflow:

1.  **Scheduler**: The `scheduler.py` script acts as the entry point, triggering the main task at a configured interval or for a single run.
2.  **Main Orchestrator (`main.py`)**: Initializes and loops through all active data providers.
3.  **Data Providers**: Each provider (`the_odds_api_provider.py`, etc.) is responsible for fetching raw data from its specific API.
4.  **Data Consolidation**: The main orchestrator gathers the structured `Game` objects from all providers into a single, unified list.
5.  **SureBet Calculator**: This powerful module iterates through every game and market, applying the correct mathematical formula to identify arbitrage opportunities.
6.  **Notifier**: If a profitable surebet is found, the `notifier.py` module formats a detailed message and sends it via the Telegram Bot API.

## ⚙️ Tech Stack

*   **Language**: Python 3.10+
*   **Core Libraries**:
    *   `requests`: For making HTTP requests to the odds APIs.
    *   `schedule`: For elegant and simple task automation.

## 🔧 Setup and Installation

Follow these steps to get the bot up and running.

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/SurebetProject.git
cd SurebetProject

```
**2. Create and Activate a Virtual Environment** (Recommended)
*   **Windows**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
*   **macOS / Linux**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**3. Install Dependencies**
This project's dependencies are listed in `requirements.txt`.
```bash
pip install -r requirements.txt
```

**4. Configure the Bot**
Rename the example configuration file `config.py.example` to `config.py` and fill in your details.
```bash
# In the terminal
mv config.py.example config.py
```

Now, open `config.py` and edit the following variables:
```python
# --- API Keys ---
# Get your key from https://the-odds-api.com/
THE_ODDS_API_KEY = "YOUR_THE_ODDS_API_KEY"

# Placeholder for the new eSports API key
ESPORTS_API_KEY = "YOUR_NEW_ESPORTS_API_KEY" 

# --- Telegram Configuration ---
# Your bot's token from BotFather
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN" 
# Your personal or group chat ID
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# --- Automation Settings ---
# Set to True to enable automated runs, False for a single manual run.
AUTOMATION_ENABLED = False
# Interval in minutes between each scan when automation is enabled.
RUN_INTERVAL_MINUTES = 60
```

## ▶️ Running the Bot

The bot can be run in two modes, controlled by the `AUTOMATION_ENABLED` flag in `config.py`.

*   **Manual Mode** (`AUTOMATION_ENABLED = False`): The bot will run a single, complete scan and then exit. This is ideal for testing.
    ```bash
    python scheduler.py
    ```

*   **Automated Mode** (`AUTOMATION_ENABLED = True`): The bot will run an initial scan and then continue to run in the background, triggering a new scan at the interval defined by `RUN_INTERVAL_MINUTES`.
    ```bash
    python scheduler.py
    ```
    For long-term running on a server, consider using a process manager like `systemd` or `supervisor`, or a simple tool like `nohup`:
    ```bash
    nohup python scheduler.py &
    ```

## 🧪 Running Tests

The project includes a dedicated test runner to validate functionality without affecting the main application.
```bash
python test_runner.py
```

You can edit this file to enable or disable specific tests for debugging providers or the calculation logic.

## 🗺️ Roadmap

This project is under active development. Future plans include:

*   **[Top Priority]** Integrate a New eSports API: Research and integrate a high-quality odds aggregator for eSports (CS2, LoL, Valorant) to achieve full market coverage.
*   **Expand Market Coverage**: Add support for more complex bet types (e.g., Asian Handicaps, Player Props).
*   **Historical Data Analysis**: Store found surebets in a database to analyze trends and bookmaker accuracy over time.
*   **Web Dashboard**: Develop a simple web interface to view bot status and historical findings.

## ⚠️ Disclaimer

This project is for educational and illustrative purposes only. The author does not guarantee profit or accept any liability for financial losses incurred by using this software. Betting involves significant financial risk. Always bet responsibly and within your means.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.





