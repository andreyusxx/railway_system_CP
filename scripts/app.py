import customtkinter as ctk
from tkinter import ttk, messagebox
# Імпортуємо ваші файли проєкту
from database import SessionLocal
from models import User, Route, Train, Ticket
import hashlib

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class RailwayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Залізнична система 2.0")
        self.geometry("400x300")
        self.state('zoomed')
        self.resizable(True, True)
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
        raw_password = self.entry_pass.get()
        # Хешуємо введений пароль алгоритмом SHA-256
        hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()
        
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.login == login).first()
            # Порівнюємо хеші
            if user and user.password == hashed_password:
                self.current_user = user
                self.login_frame.destroy()
                self.show_main_interface()
            else:
                messagebox.showerror("Помилка", "Невірний логін або пароль")
        except Exception as e:
            messagebox.showerror("Помилка БД", f"Зв'язок з базою втрачено: {e}")
        finally:
            session.close()
    def load_all_routes(self):
        """Завантажує всі рейси (скидає фільтр)"""
        for item in self.tree.get_children():
            self.tree.delete(item) # Очищаємо таблицю
            
        session = SessionLocal()
        try:
            routes = session.query(Route).all()
            for r in routes:
                train = session.query(Train).filter(Train.id == r.train_id).first()
                total = train.total_seats if train else 50  # 50 за замовчуванням

                booked = session.query(Ticket).filter(Ticket.route_id == r.id).count()

                free_seats = total - booked
                
                self.tree.insert("", "end", values=(
                    r.id, 
                    r.train_id, 
                    f"{r.departure_station}-{r.arrival_station}", 
                    r.date, 
                    r.time, 
                    f"{r.price} грн",
                    f"{free_seats} / {total}" 
                ))
        finally:
            session.close()

    def search_routes_event(self):
        """Фільтрує рейси за станцією відправлення та вираховує вільні місця"""
        search_query = self.entry_search_dep.get().strip().lower()
        if not search_query:
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        session = SessionLocal()
        try:
            routes = session.query(Route).filter(Route.departure_station.ilike(f"%{search_query}%")).all()
            for r in routes:
                train = session.query(Train).filter(Train.id == r.train_id).first()
                total = train.total_seats if train else 50
                
                booked = session.query(Ticket).filter(Ticket.route_id == r.id).count()
                
                free_seats = total - booked
                
                self.tree.insert("", "end", values=(
                    r.id, 
                    r.train_id, 
                    f"{r.departure_station}-{r.arrival_station}", 
                    r.date, 
                    r.time, 
                    f"{r.price} грн",
                    f"{free_seats} / {total}"  
                ))
        finally:
            session.close()
    def show_main_interface(self):
        """Створення веб-подібного інтерфейсу після успішного входу"""
        # 1. БІЧНА ПАНЕЛЬ (САЙДБАР)
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=("gray90", "gray15"))
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False) 

        # Логотип та інфо про поточного користувача
        ctk.CTkLabel(self.sidebar_frame, text="ЗАЛІЗНИЧНА КАСА", font=("Arial", 18, "bold"), text_color="#1F6AA5").pack(pady=(30, 5), padx=10)
        ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.current_user.login}\n({self.current_user.role})", font=("Arial", 12)).pack(pady=(0, 20), padx=10)

        # Кнопки меню для звичайних користувачів
        self.btn_schedule = ctk.CTkButton(
            self.sidebar_frame, text="📅 Розклад рейсів", anchor="w", 
            fg_color="transparent", 
            text_color=("gray10", "gray90"),      
            hover_color=("gray80", "gray25"),     
            command=self.show_schedule_page
        )
        self.btn_schedule.pack(pady=5, padx=15, fill="x")

        self.btn_profile = ctk.CTkButton(
            self.sidebar_frame, text="🎫 Мій Профіль", anchor="w", 
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray80", "gray25"), 
            command=self.show_profile_page
        )
        self.btn_profile.pack(pady=5, padx=15, fill="x")
        # Кнопки меню тільки для Адміністратора
        if self.current_user.role == "Admin":
            ctk.CTkLabel(self.sidebar_frame, text="АДМІНІСТРУВАННЯ", font=("Arial", 11, "bold"), text_color="gray50").pack(pady=(20, 5), padx=15, anchor="w")
            
            self.btn_manage = ctk.CTkButton(
                self.sidebar_frame, text="⚙️ Керування", anchor="w", 
                fg_color="transparent", 
                text_color=("gray10", "gray90"), hover_color=("gray80", "gray25"),
                command=self.show_manage_page
            )
            self.btn_manage.pack(pady=5, padx=15, fill="x")
            
            self.btn_roles = ctk.CTkButton(
                self.sidebar_frame, text="🛡️ Ролі", anchor="w", 
                fg_color="transparent", 
                text_color=("gray10", "gray90"), hover_color=("gray80", "gray25"),
                command=self.show_roles_page
            )
            self.btn_roles.pack(pady=5, padx=15, fill="x")
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.show_schedule_page()
    def clear_main_container(self):
        """Видаляє всі віджети з правої панелі перед завантаженням нової сторінки"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    def show_profile_page(self):
        """Створення інтерфейсу вкладки профілю користувача"""
        self.clear_main_container()
        # Блок інформації про користувача
        ctk.CTkLabel(self.main_container, text="ПРОФІЛЬ КОРИСТУВАЧА", font=("Arial", 16, "bold")).pack(pady=10)
        self.lbl_profile_user = ctk.CTkLabel(self.main_container, text=f"Логін: {self.current_user.login} | Роль: {self.current_user.role}", font=("Arial", 12))
        self.lbl_profile_user.pack(pady=5)
        
        ctk.CTkLabel(self.main_container, text="Історія ваших бронювань квитків:", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Таблиця куплених квитків
        columns = ("ticket_id", "route", "date", "time", "seat", "price")
        self.profile_tree = ttk.Treeview(self.main_container, columns=columns, show="headings")
        
        for col in columns:
            self.profile_tree.heading(col, text=col.capitalize())
            self.profile_tree.column(col, width=100, anchor="center")
            
        self.profile_tree.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Завантажуємо квитки
        self.load_user_tickets()

    def load_user_tickets(self):
        """Читання з БД квитків поточного користувача"""
        for item in self.profile_tree.get_children():
            self.profile_tree.delete(item)
            
        session = SessionLocal()
        try:
            # Вибираємо квитки, де user_id дорівнює id поточного користувача
            user_tickets = session.query(Ticket).filter(Ticket.user_id == self.current_user.id).all()
            for t in user_tickets:
                route = session.query(Route).filter(Route.id == t.route_id).first()
                if route:
                    self.profile_tree.insert("", "end", values=(
                        t.id,
                        f"{route.departure_station}-{route.arrival_station}",
                        route.date,
                        route.time,
                        t.seat_number,
                        f"{t.price} грн"
                    ))
        finally:
            session.close()
    def show_schedule_page(self):
        """Завантаження реальних даних з таблиці routes"""
        self.clear_main_container()
        # --- НОВА ПАНЕЛЬ ПОШУКУ ---
        search_frame = ctk.CTkFrame(self.main_container)
        search_frame.pack(pady=10, fill="x", padx=10)
        
        self.entry_search_dep = ctk.CTkEntry(search_frame, placeholder_text="Звідки (напр. Київ)")
        self.entry_search_dep.pack(side="left", padx=5)
        
        ctk.CTkButton(search_frame, text="Знайти", command=self.search_routes_event).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Скинути", fg_color="gray", command=self.load_all_routes).pack(side="left", padx=5)

        columns = ("id", "train", "route", "date", "time", "price", "seats")
        self.tree = ttk.Treeview(self.main_container, columns=columns, show="headings")
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
        self.load_all_routes()
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        ctk.CTkButton(self.main_container, text="Забронювати квиток", command=self.book_ticket_event).pack(pady=10)
    def generate_sales_report(self):
        """Логіка генерації звіту продажів"""
        session = SessionLocal()
        try:
            tickets = session.query(Ticket).all()
            total_revenue = sum([float(t.price) for t in tickets if t.price])
            
            report_filename = "Sales_Report_2026.txt"
            report_text = (
                f"=== ФІНАНСОВИЙ ЗВІТ 'ЗАЛІЗНИЧНА КАСА' ===\n"
                f"Всього продано квитків: {len(tickets)} шт.\n"
                f"Загальна виручка системи: {total_revenue} грн\n"
                f"==========================================="
            )
            with open(report_filename, "w", encoding="utf-8") as f:
                f.write(report_text)
                
            messagebox.showinfo("Звіт", f"Статистику успішно вивантажено у файл:\n{report_filename}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося згенерувати звіт: {e}")
        finally:
            session.close()
    def show_manage_page(self):
        """Сторінка керування розкладом та звітами"""
        self.clear_main_container()

        ctk.CTkLabel(self.main_container, text="Керування рейсами", font=("Arial", 18, "bold")).pack(pady=(10, 20))

        # Форма додавання рейсів
        self.entry_train_id = ctk.CTkEntry(self.main_container, placeholder_text="ID потяга", width=300)
        self.entry_train_id.pack(pady=5)
        self.entry_dep = ctk.CTkEntry(self.main_container, placeholder_text="Звідки", width=300)
        self.entry_dep.pack(pady=5)
        self.entry_arr = ctk.CTkEntry(self.main_container, placeholder_text="Куди", width=300)
        self.entry_arr.pack(pady=5)
        self.entry_date = ctk.CTkEntry(self.main_container, placeholder_text="Дата (YYYY-MM-DD)", width=300)
        self.entry_date.pack(pady=5)
        self.entry_time = ctk.CTkEntry(self.main_container, placeholder_text="Час (HH:MM)", width=300)
        self.entry_time.pack(pady=5)
        self.entry_price = ctk.CTkEntry(self.main_container, placeholder_text="Ціна (напр. 650.50)", width=300)
        self.entry_price.pack(pady=5)

        ctk.CTkButton(self.main_container, text="ЗБЕРЕГТИ РЕЙС", fg_color="green", command=self.add_route_event).pack(pady=15)

        # Кнопка для генерації звіту ідеально підходить саме для цієї сторінки
        ctk.CTkLabel(self.main_container, text="Фінансова статистика", font=("Arial", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkButton(self.main_container, text="ЗГЕНЕРУВАТИ ЗВІТ ПРОДАЖІВ", fg_color="blue", command=self.generate_sales_report).pack(pady=5)


    def show_roles_page(self):
        """Окрема сторінка керування ролями користувачів"""
        self.clear_main_container()

        ctk.CTkLabel(self.main_container, text="Керування правами доступу", font=("Arial", 18, "bold")).pack(pady=(10, 20))

        # Форма зміни ролей
        self.entry_target_user = ctk.CTkEntry(self.main_container, placeholder_text="Введіть логін користувача", width=300)
        self.entry_target_user.pack(pady=10)

        self.role_var = ctk.StringVar(value="User")
        ctk.CTkSegmentedButton(self.main_container, values=["User", "Admin"], variable=self.role_var).pack(pady=10)

        ctk.CTkButton(self.main_container, text="ОНОВИТИ ПРАВА", command=self.update_role_event).pack(pady=20)
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
                if hasattr(self, 'load_all_routes'):
                    self.load_all_routes()     
                
                if hasattr(self, 'profile_tree') and self.profile_tree.winfo_exists():
                    self.load_user_tickets()  
                invoice_filename = f"Invoice_Ticket_{new_ticket.id}.txt"
                invoice_text = (
                    f"====================================\n"
                    f"        РАХУНОК НА ОПЛАТУ №{new_ticket.id}      \n"
                    f"====================================\n"
                    f"Пасажир ID: {self.current_user.id}\n"
                    f"Рейс: {route.departure_station} - {route.arrival_station}\n"
                    f"Дата та час: {route.date} | {route.time}\n"
                    f"Місце: {new_ticket.seat_number}\n"
                    f"------------------------------------\n"
                    f"ДО СПЛАТИ: {route.price} грн\n"
                    f"===================================="
                )
                with open(invoice_filename, "w", encoding="utf-8") as f:
                    f.write(invoice_text)
                messagebox.showinfo("Успіх", f"Квиток заброньовано! Ціна: {route.price} грн")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Помилка", str(e))
        finally:
            session.close()

if __name__ == "__main__":
    app = RailwayApp()
    app.mainloop()

