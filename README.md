# JIB Price Tracker Bot

I built this bot because I was tired of manually checking GPU prices on the JIB website every day. It automatically opens a browser in the background, finds the cheapest RTX cards, and sends a notification to my Discord if the price is good.

## What it does
* **Auto-Search:** Opens JIB.co.th and searches for the GPU series I want (RTX 40/50).
* **Finds Deals:** Grabs the top 3 cheapest cards available in stock.
* **Smart Alerts:** It calculates 90% of the current cheapest price. **If any card drops below that (10% discount), it sends a Discord alert immediately.**
* **Background Mode:** Runs in "Headless Mode" so it doesn't pop up windows while I'm doing other work.

## How to use
1.  **Install requirements**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Setup Discord**
    * Create a Webhook in your Discord server.
    * Open `main.py` and paste your Webhook URL.
3.  **Run the bot**
    ```bash
    python main.py
    ```

## Tech Stack
* **Python**
* **Selenium** (for web scraping)
* **Discord Webhook** (for notifications)

