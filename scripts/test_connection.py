import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Завантажуємо змінні середовища
load_dotenv()

def test_db_connection():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5433")

    url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(url)
        with engine.connect() as connection:
            # Виконуємо простий запит для перевірки часу
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            print("\n" + "="*50)
            print("✅ ПІДКЛЮЧЕННЯ УСПІШНЕ!")
            print(f"Версія PostgreSQL: {version}")
            print("="*50 + "\n")
    except Exception as e:
        print("\n" + "="*50)
        print("❌ ПОМИЛКА ПІДКЛЮЧЕННЯ!")
        print(f"Деталі помилки: {e}")
        print("="*50 + "\n")

if __name__ == "__main__":
    test_db_connection()