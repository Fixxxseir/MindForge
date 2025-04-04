FROM python:3.12

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry

RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]