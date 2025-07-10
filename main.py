import os
import pytz
from dotenv import load_dotenv
from datetime import time

from telegram.ext import (
    ApplicationBuilder, CommandHandler, ConversationHandler,
    MessageHandler, CallbackQueryHandler, filters
)

# Load variabel dari .env
load_dotenv()
token = os.getenv("BOT_TOKEN")

# Import fungsi & state dari modul lain
from database import init_db
from handlers.start_handler import start
from handlers.today_handler import today, tomorrow, yesterday, kirim_jadwal_terjadwal
from handlers.get_handler import get_start, get_tahun, get_tanggal_bulan, cancel as cancel_get, Tahun, TanggalBulan
from handlers.maju_mundur_handler import get_plus, get_minus, proses_jumlah_hari, cancel as cancel_pm, JumlahHari
from handlers.admin_handler import admin
from handlers.donate_handler import donate
from handlers.showalluser_handler import show_all_user
from handlers.uptime_handler import uptime
from handlers.langganan_handler import langganan_today, handle_langganan_button

# Setup job queue secara async
async def setup_jobs(app):
    job_queue = app.job_queue
    job_queue.run_daily(
        kirim_jadwal_terjadwal,
        time(hour=6, minute=0, tzinfo=pytz.timezone("Asia/Jakarta"))
    )

def main():
    if not token:
        raise ValueError("BOT_TOKEN tidak ditemukan di file .env")

    # Inisialisasi DB
    init_db()

    # Buat aplikasi Telegram
    app = ApplicationBuilder().token(token).post_init(setup_jobs).build()

    # ConversationHandler untuk /get
    conv_get = ConversationHandler(
        entry_points=[CommandHandler("get", get_start)],
        states={
            Tahun: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tahun)],
            TanggalBulan: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tanggal_bulan)],
        },
        fallbacks=[CommandHandler("cancel", cancel_get)],
    )

    # ConversationHandler untuk /maju dan /mundur
    conv_pm = ConversationHandler(
        entry_points=[
            CommandHandler("maju", get_plus),
            CommandHandler("mundur", get_minus),
        ],
        states={
            JumlahHari: [MessageHandler(filters.TEXT & ~filters.COMMAND, proses_jumlah_hari)],
        },
        fallbacks=[CommandHandler("cancel", cancel_pm)],
    )

    # Daftar semua handler command
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("tomorrow", tomorrow))
    app.add_handler(CommandHandler("yesterday", yesterday))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("showalluser", show_all_user))
    app.add_handler(CommandHandler("langganan_today", langganan_today))
    app.add_handler(CommandHandler("uptime", uptime))
    app.add_handler(CallbackQueryHandler(handle_langganan_button, pattern="^langganan_"))

    # Tambahkan handler percakapan
    app.add_handler(conv_get)
    app.add_handler(conv_pm)

    print("BOT JALANNNN!!")
    app.run_polling()

if __name__ == "__main__":
    main()
