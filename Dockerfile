FROM python:3.12.2-slim
LABEL authors="sergey"

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    git \
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.2 \
  && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]