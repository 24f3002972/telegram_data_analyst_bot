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

telegram_app = Application.builder().token(BOT_TOKEN).build()


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is None:
        return

    chat_id = update.effective_chat.id
    question = update.message.text

    answer = solve(chat_id, question)

    await update.message.reply_text(answer)


telegram_app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        reply,
    )
)