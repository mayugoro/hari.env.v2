from telegram import Update
from telegram.ext import ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
image_url = os.getenv("image_url")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "Sini yg banyak🗿"
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=caption
    )
