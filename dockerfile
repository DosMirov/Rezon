FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

ENV PYTHONUNBUFFERED=1
ENV PORT=10000
ENV PYTHONPATH=/app

# 🚩 Смотри здесь — путь с папкой app!
CMD ["python", "app/main.py"]
