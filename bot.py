import telebot
import os
from PIL import Image
from io import BytesIO
import pytesseract

# Tesseract o'rnatilgan yo'lini ko'rsatish
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Telegram bot tokeni (environment variable orqali)
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

def make_docs(text):
    try:
        lines = text.split("\n")

        passport = lines[0].strip()
        name = lines[1].strip().upper().replace(" ", "/")
        birth = lines[2].strip()
        expiry = lines[3].strip()
        gender = lines[4].strip().upper()

        docs = f"SR DOCS HY HK1-P-UZB-{passport}-UZB-{birth}-{gender}-{expiry}-{name}"
        return docs

    except Exception as e:
        return f"❌ Format xato. Qaytadan tekshir.\nError: {e}"

# Matnli xabarlarni qabul qilish
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    result = make_docs(message.text)
    bot.reply_to(message, result)

# Rasmlarni qabul qilish va OCR ishlatish
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Telegramdan rasmni olish
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Rasmni PIL bilan ochish
        img = Image.open(BytesIO(downloaded_file))
        
        # OCR orqali matnni olish
        text = pytesseract.image_to_string(img, lang='eng')
        
        # SR DOCS formatiga o‘tkazish
        result = make_docs(text)
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, f"❌ Rasmni o'qishda xatolik: {e}")

# Botni ishga tushirish
bot.polling()
