-- Створення таблиці користувачів
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Створення таблиці потягів
CREATE TABLE IF NOT EXISTS trains (
    id SERIAL PRIMARY KEY,
    number VARCHAR(10) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL,
    total_seats INTEGER NOT NULL
);

-- Створення таблиці маршрутів та рейсів
CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    train_id INTEGER NOT NULL REFERENCES trains(id) ON DELETE CASCADE,
    departure_station VARCHAR(100) NOT NULL,
    arrival_station VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL
);

-- Створення таблиці квитків
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    seat_number INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);