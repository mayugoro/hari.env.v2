from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
url_admin = os.getenv("url_admin")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            text="Hubungi Admin",
            url=url_admin
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Silakan hubungi admin melalui tombol berikut:", reply_markup=reply_markup)
