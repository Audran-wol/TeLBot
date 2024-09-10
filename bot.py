import os
from pyrogram import Client, filters
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Client("forex_bot", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"))

# Function to fetch forex prices
def get_forex_prices():
    api_key = os.getenv("EXCHANGERATE_API_KEY")
    base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        forex_data = {
            "USD/EUR": data["conversion_rates"]["EUR"],
            "USD/GBP": data["conversion_rates"]["GBP"],
            "USD/JPY": data["conversion_rates"]["JPY"],
            "USD/AUD": data["conversion_rates"]["AUD"],
            "USD/CAD": data["conversion_rates"]["CAD"]
        }
        return forex_data
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return None

# Command handler for /start
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Welcome! Use /prices to get the latest forex prices.")

# Command handler for /prices
@app.on_message(filters.command("prices"))
def prices(client, message):
    forex_data = get_forex_prices()
    if forex_data:
        response_text = "Current Forex Prices:\n"
        for pair, price in forex_data.items():
            response_text += f"{pair}: {price}\n"
        response_text += "\nThis is a test application By Audran Tj 💰"
        message.reply_text(response_text)
    else:
        message.reply_text("Failed to fetch forex prices. Please try again later.")

# Run the bot
app.run()