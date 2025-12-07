from python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "if [ \"$DJANGO_ENV\" = \"dev\" ]; then python manage.py runserver 0.0.0.0:8000; else gunicorn core.wsgi:application --bind 0.0.0.0:8000; fi"]
