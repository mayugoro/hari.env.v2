from telegram import Update
from telegram.ext import ContextTypes
from database import get_all_users
import re

def escape_md(text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

async def show_all_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    if not users:
        await update.message.reply_text("Belum ada user yang terdaftar.")
        return

    pesan = "📋 *Daftar User Terdaftar:*\n\n"
    for user in users:
        raw_username = user['username'] or "-"
        username = raw_username if raw_username.startswith("@") else f"@{raw_username}"
        username = escape_md(username)
        chat_id = str(user['chat_id'])
        pesan += f"{username} : `{chat_id}`\n"

    await update.message.reply_text(pesan, parse_mode="MarkdownV2")
