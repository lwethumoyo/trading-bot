
from flask import Flask
import time
import threading
import requests
from datetime import datetime

app = Flask(__name__)

# === Your credentials here ===
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
API_KEY = "YOUR_MARKET_API_KEY"  # Replace if needed

# === Settings ===
symbols = {
    "US30": "us30",
    "NASDAQ": "nasdaq"
}

last_alert_time = {sym: datetime.min for sym in symbols}
cooldown_minutes = 15  # Alert cooldown to avoid spam

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error sending message:", e)

def check_market():
    while True:
        for name, symbol in symbols.items():
            now = datetime.now()
            if (now - last_alert_time[name]).seconds < cooldown_minutes * 60:
                continue

            # Dummy signal: alert every interval (replace with real logic)
            alert_msg = f"Signal: Check {name} now!"
            send_telegram_alert(alert_msg)
            print(alert_msg)

            last_alert_time[name] = now

        time.sleep(60)

@app.route("/")
def index():
    return "Trading Alert Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=check_market, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
