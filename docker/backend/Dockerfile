FROM python:3.11.0-alpine

# Установка рабочей директории
WORKDIR /app

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновление PIP и установка нужных зависимостей
RUN pip install --upgrade pip
RUN pip install gunicorn
COPY ../../requirements.txt .
RUN pip install -r requirements.txt

COPY ../.. .

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
