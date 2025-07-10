from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import datetime
from utils import bulan_masehi_id, get_pasaran_jawa, escape_markdown_v2

JumlahHari = 0

async def get_plus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['arah'] = 'plus'
    await update.message.reply_text("Mau maju berapa hari?")
    return JumlahHari

async def get_minus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['arah'] = 'minus'
    await update.message.reply_text("Mau mundur berapa hari?")
    return JumlahHari

async def proses_jumlah_hari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jumlah = update.message.text.strip()
    if not jumlah.isdigit():
        await update.message.reply_text("Masukkan jumlah hari dalam angka.")
        return JumlahHari

    jumlah = int(jumlah)
    arah = context.user_data.get('arah')
    today = datetime.date.today()
    tanggal_target = today + datetime.timedelta(days=jumlah) if arah == 'plus' else today - datetime.timedelta(days=jumlah)
    return await kirim_detail_tanggal(update, context, tanggal_target)

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
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Perintah dibatalkan.")
    return ConversationHandler.END
