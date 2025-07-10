from telegram import Update
from telegram.ext import ContextTypes
from database import save_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user)

    welcome_text = (
        "Halo! 👋🗿\n"
        "Selamat datang di bot cek hari dan tanggal.\n\n"
        "Kamu bisa gunakan perintah seperti:\n"
        "/today - Lihat info hari ini\n"
        "/tomorrow - Info besok\n"
        "/yesterday - Info kemarin\n"
        "/get - Cek hari dari tanggal tertentu\n"
        "/maju - Tambah hari ke depan\n"
        "/mundur - Mundur beberapa hari\n"
        "/langganan_today - Jadwalkan info otomatis jam 6 pagi\n"
        "/donate - Bantu support bot ini\n"
        "/admin - Kontak admin\n"
    )
    await update.message.reply_text(welcome_text)
