from telegram import Update
from telegram.ext import ContextTypes
import time
import asyncio

# Simpan waktu mulai bot
BOT_START_TIME = time.time()

def get_uptime():
    durasi = int(time.time() - BOT_START_TIME)

    hari = durasi // 86400
    sisa = durasi % 86400
    jam = sisa // 3600
    menit = (sisa % 3600) // 60
    detik = sisa % 60

    parts = []
    if hari > 0: parts.append(f"{hari} Hari")
    if jam > 0: parts.append(f"{jam} jam")
    if menit > 0: parts.append(f"{menit} menit")
    if detik > 0: parts.append(f"{detik} detik")

    return " ".join(parts)

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    durasi = get_uptime()
    msg = await update.message.reply_text(f"🕒 Bot sudah online selama: {durasi}")

    # Tunggu 10 detik, lalu hapus pesan bot & pesan user
    await asyncio.sleep(10)
    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=msg.message_id)
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    except:
        pass
