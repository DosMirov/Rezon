FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

ENV PYTHONUNBUFFERED=1
ENV PORT=10000
ENV PYTHONPATH=/app

# Проверка на присутствие функции set_state в app/session.py (build-time sanity check)
RUN python - <<'PY'
import importlib
m = importlib.import_module("app.session")
assert hasattr(m, "set_state"), "Docker-context урезан: в app/session.py нет set_state"
PY

CMD ["python", "app/main.py"]
