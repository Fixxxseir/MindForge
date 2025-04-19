FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-root --no-interaction --no-ansi

COPY . .

RUN mkdir -p /app/staticfiles /app/media && \
    chown -R 1000:1000 /app/staticfiles /app/media && \
    chmod -R 755 /app/staticfiles /app/media

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]