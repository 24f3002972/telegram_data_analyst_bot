import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request, send_file, abort

from telegram import Update

from bot import telegram_app

load_dotenv()

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

    return send_file(LOG_FILE)


@app.post("/webhook")
async def webhook():

    data = request.get_json(force=True)

    update = Update.de_json(data, telegram_app.bot)

    await telegram_app.process_update(update)

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
