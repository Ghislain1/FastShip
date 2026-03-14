# 1. Use a lightweight Python base image
FROM python:3.11-slim

# 2. set work directory in the container 
WORKDIR /app

COPY requirements.txt  .

RUN  pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
