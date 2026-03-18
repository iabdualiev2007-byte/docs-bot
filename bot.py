import telebot
import os

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

    except:
        return "❌ Format xato. Qaytadan tekshir."

@bot.message_handler(func=lambda message: True)
def handle(message):
    result = make_docs(message.text)
    bot.reply_to(message, result)

bot.polling()
