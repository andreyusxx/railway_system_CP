# Використовуємо офіційний образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Оновлюємо pip та встановлюємо необхідні бібліотеки
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли проєкту
COPY . .
