import telebot
import os
from PIL import Image
import pytesseract
from io import BytesIO

# TOKEN environment variable orqali olinadi
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Passportdan ma'lumot ajratish funksiyasi
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

# Rasmdan matn olish funksiyasi
def ocr_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image, lang='eng')
    return text

# Matnli xabarlar handleri
@bot.message_handler(content_types=['text'])
def handle_text(message):
    result = make_docs_from_text(message.text)
    bot.reply_to(message, result)

# Rasmli xabarlar handleri
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Telegram serveridan rasmni olish
        file_info = bot.get_file(message.photo[-1].file_id)
        file = bot.download_file(file_info.file_path)
        file_bytes = BytesIO(file)

        # OCR orqali matn olish
        text = ocr_image(file_bytes)
        result = make_docs_from_text(text)
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {str(e)}")

# Botni ishga tushirish
bot.polling()
