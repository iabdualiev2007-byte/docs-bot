# 1️⃣ Boshlang'ich image sifatida Python 3.13 slim ishlatiladi
FROM python:3.13-slim

# 2️⃣ System update va Tesseract OCR o'rnatish
RUN apt-get update && apt-get install -y tesseract-ocr

# 3️⃣ Ish papkasini yaratish va unga kirish
WORKDIR /app

# 4️⃣ Python kutubxonalarini o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Barcha loyiha fayllarini container ichiga nusxalash
COPY . .

# 6️⃣ Botni ishga tushirish
CMD ["python", "bot.py"]
