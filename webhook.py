import os
import json

from flask import Flask, request

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()