from flask import Flask, send_file
from threading import Thread
from pathlib import Path

from bot import telegram_app

app = Flask(__name__)

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "run.jsonl"


@app.get("/")
def home():
    return "Telegram Data Analyst Bot is running."


@app.get("/run.jsonl")
def run_log():
    LOG_DIR.mkdir(exist_ok=True)

    if not LOG_FILE.exists():
        LOG_FILE.write_text("", encoding="utf-8")

    return send_file(LOG_FILE, mimetype="application/json")

def start_bot():
    telegram_app.run_polling(
        stop_signals=None
    )


if __name__ == "__main__":
    Thread(target=start_bot, daemon=True).start()

    app.run(
        host="0.0.0.0",
        port=5000,
    )