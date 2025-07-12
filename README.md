# Rezon Voice Bot

Telegram bot for collecting voice fragments from users and forwarding them to an admin channel.

## 🚀 Features

- `/start` — begins a new “brief” session and returns Brief-ID.
- Voice messages are logged atomically (fragment index + metadata).
- `/done` or “Завершить” button — closes the session.
- Stored in SQLite; can be swapped to Supabase/Firebase later.
- Minimalist UX; metadata tags added to each forwarded fragment.

## 📁 Project Structure

```

.
├── app
│   ├── bot.py                # singleton Bot and Dispatcher
│   ├── config.py             # Pydantic settings loader
│   ├── main.py               # aiohttp webhook server (entrypoint)
│   ├── handlers              # user-flow routers
│   │   ├── register.py
│   │   ├── start.py
│   │   ├── voice.py
│   │   └── complete.py
│   ├── services
│   │   └── send\_to\_channel.py
│   ├── storage
│   │   ├── db.py             # schema init
│   │   └── repository.py     # atomic data layer
│   └── utils
│       └── time.py           # timestamp helpers
├── Dockerfile
├── requirements.txt
├── runtime.txt               # (can be removed if unused)
└── .env.sample

````

## 🔧 Getting Started

1. **Clone repository**  
   ```bash
   git clone https://github.com/your/repo.git
   cd repo
````

2. **Create virtual environment & install deps**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure**

   * Copy `.env.sample` → `.env`
   * Fill in `BOT_TOKEN`, `CHANNEL_ID`, `BASE_WEBHOOK_URL`, etc.

4. **Initialize database**
   (Handled automatically on startup)

5. **Run locally**

   ```bash
   # for webhook mode, expose via ngrok or similar:
   ngrok http 10000
   # set NGROK_URL and WEBHOOK_PATH in .env
   python -m app.main
   ```

6. **Deploy with Docker**

   ```bash
   docker build -t rezon-voice-bot .
   docker run -e BOT_TOKEN=… \
              -e CHANNEL_ID=… \
              -e BASE_WEBHOOK_URL=… \
              -e WEBHOOK_PATH=/webhook \
              -e DATABASE_PATH=./rezon.db \
              -p 10000:10000 \
              rezon-voice-bot
   ```

7. **Zeabur Deployment**

   * Push to repo; set env vars in Zeabur dashboard.
   * Ensure `PORT=10000` is set.
   * Verify `/health` or `/` returns “Bot is up.”
   * In Telegram, call `getWebhookInfo` to confirm webhook URL.

## 🛠️ Future Improvements

* Swap `MemoryStorage` → `RedisStorage` for horizontal scaling.
* Add FastAPI-based admin panel for exporting sessions.
* Move `send_to_channel` to background queue with retries.
* Integrate Supabase/Firebase for long-term storage.

