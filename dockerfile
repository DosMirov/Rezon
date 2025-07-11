# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы
COPY . .

# Экспонируем порт (важно для Zeabur и Fly.io)
EXPOSE 10000

# Устанавливаем переменные окружения
ENV PORT=10000
ENV PYTHONUNBUFFERED=1

# Стартовое приложение
CMD ["python", "app/bot.py"]