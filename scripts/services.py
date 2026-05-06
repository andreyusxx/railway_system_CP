class BookingService:
    def __init__(self, repository):
        self.repo = repository

    def find_and_book_ticket(self, user_login, route_id, seat_number, price):
        user = self.repo.get_user_by_login(user_login)
        if not user:
            raise ValueError("Користувача не знайдено.")
        
        # Створюємо бронювання квитка
        ticket = self.repo.book_ticket(
            user_id=user.id,
            route_id=route_id,
            seat_number=seat_number,
            price=price
        )
        return ticket