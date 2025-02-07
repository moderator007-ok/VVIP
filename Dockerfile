FROM python:3.12.1
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r master.txt

CMD gunicorn app:app & python3 main.py
