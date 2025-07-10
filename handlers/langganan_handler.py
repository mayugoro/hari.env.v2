from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import update_subscription

async def langganan_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Ya", callback_data="langganan_yes")],
        [InlineKeyboardButton("❌ Tidak", callback_data="langganan_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Kamu ingin menerima detail hari setiap pagi jam 06:00 WIB?",
        reply_markup=reply_markup
    )

async def handle_langganan_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data == "langganan_yes":
        update_subscription(chat_id, True)
        await query.edit_message_text("✅ Kamu akan menerima detail hari setiap pagi jam 06:00.")
    elif query.data == "langganan_no":
        update_subscription(chat_id, False)
        await query.edit_message_text("❌ Langganan detail harian dihentikan.")
