# Python 3.11 slim imidjidan foydalanamiz
FROM python:3.11-slim

# Ishchi katalogni yaratish
WORKDIR /app

# Sistemaga zarur paketlar
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Requirements faylini konteynerga nusxalash
COPY requirements.txt .

# Pipni yangilash va paketlarni o'rnatish (timeout oshirilgan)
RUN pip install --upgrade pip \
    && pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Loyiha fayllarini konteynerga nusxalash
COPY . .

# Django runserver port
EXPOSE 8000

# Konteyner ishga tushganda bajariladigan buyruq
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
