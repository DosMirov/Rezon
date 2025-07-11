import time
import requests

URL = "https://rezon-voice-bot.onrender.com/health"

while True:
    try:
        r = requests.get(URL, timeout=5)
        print("✅ Ping OK:", r.status_code)
    except Exception as e:
        print("❌ Ping failed:", e)
    time.sleep(600)  # 10 минут