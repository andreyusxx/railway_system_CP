# Використовуємо офіційний образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Оновлюємо pip та встановлюємо необхідні бібліотеки
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли проєкту
COPY . .

EXPOSE 8000

# Команда для запуску 
CMD ["python", "app.py"]