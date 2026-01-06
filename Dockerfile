# Берём Python 3.11
FROM python:3.11-slim

# Рабочая папка
WORKDIR /app

# Копируем зависимости и код
COPY requirements.txt .
COPY kava_bot.py .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Запуск бота
CMD ["python", "kava_bot.py"]
