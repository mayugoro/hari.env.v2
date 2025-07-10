from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import datetime
from utils import bulan_to_number, bulan_masehi_id, get_pasaran_jawa, escape_markdown_v2

Tahun, TanggalBulan = range(2)

async def get_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_bot = await update.message.reply_text("Masukkan tahun :")
    context.user_data['messages_to_delete'] = [msg_bot.message_id, update.message.message_id]
    return Tahun

async def get_tahun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tahun = update.message.text.strip()
    if not tahun.isdigit():
        await update.message.reply_text("Tahun harus berupa angka. Silakan coba lagi:")
        context.user_data['messages_to_delete'].append(update.message.message_id)
        return Tahun

    context.user_data['tahun'] = int(tahun)
    msg_bot = await update.message.reply_text("Masukkan tanggal dan bulan :")
    context.user_data['messages_to_delete'].extend([msg_bot.message_id, update.message.message_id])
    return TanggalBulan

async def get_tanggal_bulan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    parts = text.split()
    if len(parts) != 2:
        await update.message.reply_text("Format salah. Contoh yang benar: 1 mei")
        context.user_data['messages_to_delete'].append(update.message.message_id)
        return TanggalBulan

    tanggal_str, bulan_str = parts
    if not tanggal_str.isdigit():
        await update.message.reply_text("Tanggal harus angka. Contoh: 1 mei")
        context.user_data['messages_to_delete'].append(update.message.message_id)
        return TanggalBulan

    tanggal = int(tanggal_str)
    bulan = bulan_to_number(bulan_str)
    if bulan == 0:
        await update.message.reply_text("Nama bulan tidak valid. Contoh: januari, februari, mei, dll.")
        context.user_data['messages_to_delete'].append(update.message.message_id)
        return TanggalBulan

    tahun = context.user_data.get('tahun')
    if not tahun:
        await update.message.reply_text("Terjadi kesalahan. Silakan mulai ulang dengan /get")
        return ConversationHandler.END

    try:
        tanggal_input = datetime.date(tahun, bulan, tanggal)
    except ValueError:
        await update.message.reply_text("Tanggal tidak valid untuk bulan tersebut. Silakan coba lagi:")
        context.user_data['messages_to_delete'].append(update.message.message_id)
        return TanggalBulan

    return await kirim_detail_tanggal(update, context, tanggal_input)

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

    chat_id = update.effective_chat.id
    for msg_id in context.user_data.get('messages_to_delete', []):
        try:
            if msg_id != update.message.message_id:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except:
            pass

    await update.message.reply_text(pesan, parse_mode="MarkdownV2")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Perintah dibatalkan.")
    return ConversationHandler.END
