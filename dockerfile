# syntax=docker/dockerfile:1

# ✅ 1. Используем минимальный Python-образ
FROM python:3.11-slim

# ✅ 2. Создаём рабочую директорию ВНУТРИ образа
WORKDIR /app

# ✅ 3. Копируем зависимости отдельно (для кэширования)
COPY requirements.txt .

# ✅ 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 5. Копируем весь код внутрь /app (включая папку `app/`)
COPY . .

# ✅ 6. Указываем порт для запуска
EXPOSE 10000

# ✅ 7. Устанавливаем переменные окружения (если нужно)
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# ✅ 8. Стартуем бот через python
CMD ["python", "app/main.py"]
