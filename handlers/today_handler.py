from telegram import Update
from telegram.ext import ContextTypes
import datetime
import pytz
from utils import get_pasaran_jawa, bulan_masehi_id, escape_markdown_v2
from database import get_subscribed_chat_ids

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz = pytz.timezone("Asia/Jakarta")
    now = datetime.datetime.now(tz).date()
    await kirim_detail_tanggal(update, context, now)

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz = pytz.timezone("Asia/Jakarta")
    besok = datetime.datetime.now(tz).date() + datetime.timedelta(days=1)
    await kirim_detail_tanggal(update, context, besok)

async def yesterday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz = pytz.timezone("Asia/Jakarta")
    kemarin = datetime.datetime.now(tz).date() - datetime.timedelta(days=1)
    await kirim_detail_tanggal(update, context, kemarin)

async def kirim_detail_tanggal(update: Update, context: ContextTypes.DEFAULT_TYPE, tanggal_input: datetime.date):
    jam = datetime.datetime.now().strftime("%H:%M:%S")
    tanggal_jawa = get_pasaran_jawa(tanggal_input)
    hari_indonesia = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu",
        "Sunday": "Minggu",
    }
    hari = hari_indonesia.get(tanggal_input.strftime("%A"), tanggal_input.strftime("%A"))
    tanggal_masehi = f"{tanggal_input.day} {bulan_masehi_id(tanggal_input.month)}"
    judul = "✨ DETAIL HARI ✨"

    pesan = (
        f"`{judul}`\n\n"
        f"🧮 `Tahun           : {tanggal_input.year}`\n"
        f"💌 `Hari            : {hari}`\n"
        f"💌 `Tanggal Masehi  : {tanggal_masehi}`\n"
        f"📧 `Tanggal Jawa    : {tanggal_jawa}`\n"
        f"⌚ `Jam             : {jam}`"
    )
    pesan = escape_markdown_v2(pesan)
    await update.message.reply_text(pesan, parse_mode="MarkdownV2")

# Fungsi kirim otomatis ke user yang berlangganan
async def kirim_jadwal_terjadwal(context: ContextTypes.DEFAULT_TYPE):
    tz = pytz.timezone("Asia/Jakarta")
    now = datetime.datetime.now(tz)
    tanggal_input = now.date()
    jam = now.strftime("%H:%M:%S")
    tanggal_jawa = get_pasaran_jawa(tanggal_input)

    hari_indonesia = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu",
        "Sunday": "Minggu",
    }
    hari = hari_indonesia.get(tanggal_input.strftime("%A"), tanggal_input.strftime("%A"))
    tanggal_masehi = f"{tanggal_input.day} {bulan_masehi_id(tanggal_input.month)}"
    judul = "✨ DETAIL HARI ✨"

    pesan = (
        f"`{judul}`\n\n"
        f"🧮 `Tahun           : {tanggal_input.year}`\n"
        f"💌 `Hari            : {hari}`\n"
        f"💌 `Tanggal Masehi  : {tanggal_masehi}`\n"
        f"📧 `Tanggal Jawa    : {tanggal_jawa}`\n"
        f"⌚ `Jam             : {jam}`"
    )
    pesan = escape_markdown_v2(pesan)

    for chat_id in get_subscribed_chat_ids():
        try:
            await context.bot.send_message(chat_id=chat_id, text=pesan, parse_mode="MarkdownV2")
        except Exception as e:
            print(f"Gagal kirim ke {chat_id}: {e}")
