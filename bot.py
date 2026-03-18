import telebot
import os
from PIL import Image
import pytesseract
from io import BytesIO
import requests

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Tesseract yo'lini ko'rsatish (agar PATH qo'shilmagan bo'lsa)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def make_docs_from_text(text):
    try:
        lines = text.split("\n")
        passport = lines[0].strip()
        name = lines[1].strip().upper().replace(" ", "/")
        birth = lines[2].strip()
        expiry = lines[3].strip()
        gender = lines[4].strip().upper()
        docs = f"SR DOCS HY HK1-P-UZB-{passport}-UZB-{birth}-{gender}-{expiry}-{name}"
        return docs
    except:
        return "❌ Format xato. Qaytadan tekshir."

# Rasm qabul qiluvchi handler
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
        response = requests.get(file_url)
        img = Image.open(BytesIO(response.content))

        # OCR bilan text olish
        text = pytesseract.image_to_string(img)
        result = make_docs_from_text(text)
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {e}")

bot.polling()
