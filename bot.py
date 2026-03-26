import telebot
import os
from PIL import Image
from io import BytesIO
import pytesseract
from dotenv import load_dotenv
import cv2
import numpy as np

# .env faylidan tokenni olish
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Telegram bot yaratish
bot = telebot.TeleBot(TOKEN)

# Railway server va lokal uchun Tesseract path
pytesseract.pytesseract.tesseract_cmd = os.environ.get("TESSERACT_CMD") or "tesseract"

# Rasmni preprocess qilish funksiyasi (OCR uchun)
def preprocess_image(img):
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# SR DOCS formatini yaratish funksiyasi
def make_docs(text):
    try:
        lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
        passport = lines[0]                         # Pasport raqami
        name = lines[1].upper().replace(" ", "/")   # Ism va familiya
        birth = lines[2]                            # Tug‘ilgan sana
        expiry = lines[3]                           # Amal qilish muddati
        gender = lines[4].upper()                   # Jins (M/F)
        docs = f"SRDOCSHK1-P/UZB/{passport}/UZB/{birth}/{gender}/{expiry}/{name}"
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
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = Image.open(BytesIO(downloaded_file))

        # Preprocess va OCR
        processed_img = preprocess_image(img)
        text = pytesseract.image_to_string(processed_img, lang='eng')

        result = make_docs(text)
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, f"❌ Rasmni o'qishda xatolik: {e}")

# Botni ishga tushirish
print("📌 Docs-Bot ishga tushdi...")
bot.infinity_polling()
