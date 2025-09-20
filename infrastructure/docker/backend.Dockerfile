FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/pyproject.toml backend/README.md ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir hatchling

COPY backend ./
RUN pip install --no-cache-dir .

ENV APP_ENV=container \
    APP_API_PREFIX=/api \
    APP_API_VERSION=v1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
