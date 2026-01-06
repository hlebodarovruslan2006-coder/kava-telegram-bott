# Используем Python 3.11
FROM python:3.11-slim

# Рабочая директория в контейнере
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
COPY kava_bot.py .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска бота
CMD ["python", "kava_bot.py"]
