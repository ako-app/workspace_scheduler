FROM python:3.14

RUN pip install --no-cache-dir "poetry==2.4.1"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-root --only main

COPY . .

RUN useradd --create-home appuser
USER appuser

CMD [ "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]