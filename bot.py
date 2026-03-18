import telebot
import os
from PIL import Image
from io import BytesIO
import pytesseract
from dotenv import load_dotenv

# .env faylidan tokenni olish
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Telegram bot yaratish
bot = telebot.TeleBot(TOKEN)

# Windows uchun Tesseract yo'li
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# SR DOCS formatini yaratish funksiyasi
def make_docs(text):
    try:
        # Bo‘sh qatordan xalos bo‘lish
        lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
        
        passport = lines[0]         # Pasport raqami
        name = lines[1].upper().replace(" ", "/")  # Ism va familiya
        birth = lines[2]            # Tug‘ilgan sana
        expiry = lines[3]           # Amal qilish muddati
        gender = lines[4].upper()   # Jins

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
