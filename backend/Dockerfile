FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS test

COPY . .

ENV DATABASE_URL=sqlite+aiosqlite:///./test.db

RUN pytest -v --tb=short

FROM base AS production

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

USER nobody

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
