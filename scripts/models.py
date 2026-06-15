from sqlalchemy import Column, Integer, String, Date, Time, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)

class Train(Base):
    __tablename__ = 'trains'
    id = Column(Integer, primary_key=True)
    number = Column(String(10), unique=True, nullable=False)
    type = Column(String(50), nullable=False)
    total_seats = Column(Integer, nullable=False)

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey('trains.id', ondelete="CASCADE"), nullable=False)
    departure_station = Column(String(100), nullable=False)
    arrival_station = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    price = Column(Numeric(10, 2), default=0.00)

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey('routes.id', ondelete="CASCADE"), nullable=False)
    seat_number = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2))