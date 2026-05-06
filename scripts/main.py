from database import engine, init_db
from models import Base

def main():
    # Створюємо таблиці в базі даних, якщо вони ще не створені
    print("Ініціалізація бази даних...")
    init_db()
    print("Таблиці успішно створено!")

if __name__ == "__main__":
    main()