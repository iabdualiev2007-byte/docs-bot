import telebot
import os
from PIL import Image
from io import BytesIO
import pytesseract
import requests

# ==========================
# Telegram bot token va chat ID
# ==========================
TOKEN = "7579110371:AAGy6n38FH1FvHdHJ600LE4q2WFvJzu3P_A"

bot = telebot.TeleBot(TOKEN)

# ==========================
# Railway / Linux uchun Tesseract path
# ==========================
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# ==========================
# Matnni maxsus formatga o'zgartirish funksiyasi
# ==========================
def make_docs(text):
    try:
        lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
        passport = lines[0]
        name = lines[1].upper().replace(" ", "/")
        birth = lines[2]
        expiry = lines[3]
        gender = lines[4].upper()
        docs = f"SRDOCSHK1-P/UZB/{passport}/UZB/{birth}/{gender}/{expiry}/{name}"
        return docs
    except Exception as e:
        return f"❌ Format xato. Qaytadan tekshir.\nError: {e}"

# ==========================
# Text xabar qabul qilish
# ==========================
@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(message):
    result = make_docs(message.text)
    bot.reply_to(message, result)

# ==========================
# Photo xabar qabul qilish
# ==========================
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = Image.open(BytesIO(downloaded_file))
        text = pytesseract.image_to_string(img, lang='eng')
        result = make_docs(text)
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, f"❌ Rasmni o'qishda xatolik: {e}")

# ==========================
# Bot ishga tushishi
# ==========================
print("📌 Docs-Bot ishga tushdi...")
bot.infinity_polling()
