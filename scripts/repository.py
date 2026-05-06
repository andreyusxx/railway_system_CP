from sqlalchemy.orm import Session
from models import User, Train, Route, Ticket

class DatabaseRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    # Операції для користувачів
    def create_user(self, login, password, role):
        new_user = User(login=login, password=password, role=role)
        self.db.add(new_user)
        self.db.commit()
        return new_user

    def get_user_by_login(self, login):
        return self.db.query(User).filter(User.login == login).first()

    def update_user_password(self, user_id, new_password):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.password = new_password
            self.db.commit()
        return user

    def delete_user(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
        return user

    # Операції для рейсів та квитків
    def get_all_routes(self):
        return self.db.query(Route).all()

    def book_ticket(self, user_id, route_id, seat_number, price):
        new_ticket = Ticket(user_id=user_id, route_id=route_id, seat_number=seat_number, price=price)
        self.db.add(new_ticket)
        self.db.commit()
        return new_ticket