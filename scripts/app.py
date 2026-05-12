import customtkinter as ctk
from tkinter import ttk, messagebox
# Імпортуємо ваші файли проєкту
from database import SessionLocal
from models import User, Route, Train, Ticket

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class RailwayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Залізнична система 2.0")
        self.geometry("400x300")
        self.resizable(False, False)
        self.current_user = None
        self.show_login_screen()

    def show_login_screen(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)
        ctk.CTkLabel(self.login_frame, text="ВХІД", font=("Arial", 20, "bold")).pack(pady=10)
        self.entry_login = ctk.CTkEntry(self.login_frame, placeholder_text="Логін")
        self.entry_login.pack(pady=10)
        self.entry_pass = ctk.CTkEntry(self.login_frame, placeholder_text="Пароль", show="*")
        self.entry_pass.pack(pady=10)
        ctk.CTkButton(self.login_frame, text="Увійти", command=self.authenticate).pack(pady=20)

    def authenticate(self):
        """Реальна перевірка користувача через базу даних"""
        login = self.entry_login.get()
        password = self.entry_pass.get()

        session = SessionLocal()
        try:
            user = session.query(User).filter(User.login == login).first()
            if user and user.password == password: # У продакшні тут має бути хеш!
                self.current_user = user
                self.login_frame.destroy()
                self.show_main_interface()
            else:
                messagebox.showerror("Помилка", "Невірний логін або пароль")
        except Exception as e:
            messagebox.showerror("Помилка БД", f"Зв'язок з базою втрачено: {e}")
        finally:
            session.close()

    def show_main_interface(self):
        self.geometry("900x600")
        self.resizable(True, True)
        
        # Використовуємо об'єкт користувача з БД
        self.info_label = ctk.CTkLabel(self, text=f"Користувач: {self.current_user.login} | Роль: {self.current_user.role}")
        self.info_label.pack(pady=5, padx=20, anchor="e")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=10, padx=20, fill="both", expand=True)

        self.tabview.add("Розклад")
        self.setup_schedule_tab()

        if self.current_user.role == "Admin":
            self.tabview.add("Керування")
            self.tabview.add("Ролі")
            self.setup_admin_tabs()

    def setup_schedule_tab(self):
        """Завантаження реальних даних з таблиці routes"""
        columns = ("id", "train", "route", "date", "time", "price")
        self.tree = ttk.Treeview(self.tabview.tab("Розклад"), columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            # Можна трохи звузити колонку ціни
            if col == "price":
                self.tree.column(col, width=100, anchor="center")
        
        session = SessionLocal()
        try:
            routes = session.query(Route).all()
            for r in routes:
                self.tree.insert("", "end", values=(
                    r.id, 
                    r.train_id, 
                    f"{r.departure_station}-{r.arrival_station}", 
                    r.date, 
                    r.time,
                    f"{r.price} грн" 
                ))
        finally:
            session.close()
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        ctk.CTkButton(self.tabview.tab("Розклад"), text="Забронювати квиток", command=self.book_ticket_event).pack(pady=10)

    def setup_admin_tabs(self):
        """Повноцінний адмін-функціонал"""
        # Керування рейсами
        tab = self.tabview.tab("Керування")
        self.entry_train_id = ctk.CTkEntry(tab, placeholder_text="ID потяга", width=300)
        self.entry_train_id.pack(pady=5)
        self.entry_dep = ctk.CTkEntry(tab, placeholder_text="Звідки", width=300)
        self.entry_dep.pack(pady=5)
        self.entry_arr = ctk.CTkEntry(tab, placeholder_text="Куди", width=300)
        self.entry_arr.pack(pady=5)
        self.entry_date = ctk.CTkEntry(tab, placeholder_text="Дата (YYYY-MM-DD)", width=300)
        self.entry_date.pack(pady=5)
        self.entry_time = ctk.CTkEntry(tab, placeholder_text="Час (HH:MM)", width=300)
        self.entry_time.pack(pady=5)
        self.entry_price = ctk.CTkEntry(tab, placeholder_text="Ціна (напр. 650.50)", width=300)
        self.entry_price.pack(pady=5)

        ctk.CTkButton(tab, text="ЗБЕРЕГТИ РЕЙС", fg_color="green", 
                      command=self.add_route_event).pack(pady=20)
        

        # Ролі
        role_tab = self.tabview.tab("Ролі")
        self.entry_target_user = ctk.CTkEntry(role_tab, placeholder_text="Логін")
        self.entry_target_user.pack(pady=5)
        self.role_var = ctk.StringVar(value="User")
        ctk.CTkSegmentedButton(role_tab, values=["User", "Admin"], variable=self.role_var).pack(pady=10)
        ctk.CTkButton(role_tab, text="ОНОВИТИ ПРАВА", command=self.update_role_event).pack(pady=10)

    def add_route_event(self):
        """Логіка збереження в БД"""
        session = SessionLocal()
        try:
            price_val = float(self.entry_price.get())
            new_route = Route(
                train_id=int(self.entry_train_id.get()),
                departure_station=self.entry_dep.get(),
                arrival_station=self.entry_arr.get(),
                date=self.entry_date.get(),
                time=self.entry_time.get(),
                price=price_val
            )
            session.add(new_route)
            session.commit()
            messagebox.showinfo("Успіх", f"Рейс на {new_route.date} о {new_route.time} додано!")
            
            # Очищуємо поля після успіху
            self.entry_price.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Помилка", "Будь ласка, введіть коректне число у поле ціни")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Помилка", str(e))
        finally:
            session.close()

    def update_role_event(self):
        target_login = self.entry_target_user.get()
        new_role = self.role_var.get()
        
        if not target_login:
            messagebox.showwarning("Увага", "Введіть логін користувача")
            return

        session = SessionLocal()
        try:
            # Шукаємо користувача за логіном
            user_to_update = session.query(User).filter(User.login == target_login).first()
            
            if user_to_update:
                user_to_update.role = new_role
                session.commit()
                messagebox.showinfo("Успіх", f"Роль користувача {target_login} змінено на {new_role}")
                self.entry_target_user.delete(0, 'end')
            else:
                messagebox.showwarning("Помилка", f"Користувача з логіном '{target_login}' не знайдено")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Помилка БД", f"Не вдалося оновити роль: {e}")
        finally:
            session.close()
    def book_ticket_event(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Увага", "Виберіть рейс")
            return

        # Отримуємо дані вибраного рейсу з таблиці
        values = self.tree.item(selected_item)['values']
        route_id = values[0]

        session = SessionLocal()
        try:
            # Знаходимо цей рейс у базі, щоб дізнатися його ціну
            route = session.query(Route).filter(Route.id == int(route_id)).first()
            
            if route:
                new_ticket = Ticket(
                    route_id=route.id,
                    user_id=self.current_user.id,
                    seat_number=1,
                    price=route.price 
                )
                session.add(new_ticket)
                session.commit()
                messagebox.showinfo("Успіх", f"Квиток заброньовано! Ціна: {route.price} грн")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Помилка", str(e))
        finally:
            session.close()

if __name__ == "__main__":
    app = RailwayApp()
    app.mainloop()