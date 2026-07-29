import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)

from analysis_engine import solve

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    question = update.message.text

    answer = solve(chat_id, question)

    await update.message.reply_text(answer)


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        reply,
    )
)

print("Bot initialized.")

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()