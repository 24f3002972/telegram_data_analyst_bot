from flask import Flask, send_file
import threading

from bot import app as telegram_app

app = Flask(__name__)


@app.get("/")
def home():
    return "Telegram Data Analyst Bot is running."


@app.get("/run.jsonl")
def logs():
    return send_file(
        "logs/run.jsonl",
        mimetype="application/json"
    )


def run_bot():
    telegram_app.run_polling()


threading.Thread(
    target=run_bot,
    daemon=True,
).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    