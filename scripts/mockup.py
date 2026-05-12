import customtkinter as ctk
from tkinter import ttk

# Налаштування світлої теми
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Railway System - Панель керування")
        self.geometry("900x600")
        self.configure(fg_color="#FFFFFF") 

        # 1. Створення вкладок
        self.tabview = ctk.CTkTabview(self, width=850, height=550, fg_color="#F2F2F2")
        self.tabview.pack(pady=20, padx=20)

        self.tabview.add("Квитки")
        self.tabview.add("Додати дані")
        self.tabview.add("Редагування")
        self.tabview.add("Ролі")

        self.setup_tickets_tab()
        self.setup_add_data_tab()
        self.setup_edit_tab()
        self.setup_roles_tab()

    def setup_tickets_tab(self):
        """Сторінка перегляду даних (Світла тема)"""
        label = ctk.CTkLabel(self.tabview.tab("Квитки"), text="Перегляд активних рейсів", 
                             font=("Arial", 20, "bold"), text_color="#1A1A1A")
        label.pack(pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="white", 
                        foreground="black", 
                        fieldbackground="white", 
                        rowheight=25)
        style.map("Treeview", background=[('selected', '#3B8ED0')])
        
        columns = ("id", "train", "route", "date", "price")
        self.tree = ttk.Treeview(self.tabview.tab("Квитки"), columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("train", text="Потяг")
        self.tree.heading("route", text="Маршрут")
        self.tree.heading("date", text="Дата")
        self.tree.heading("price", text="Ціна")

        data = [("1", "705К", "Київ - Львів", "2026-05-15", "650 грн"),
                ("2", "012Л", "Київ - Одеса", "2026-05-16", "480 грн")]
        
        for item in data:
            self.tree.insert("", "end", values=item)
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        btn = ctk.CTkButton(self.tabview.tab("Квитки"), text="Забронювати квиток")
        btn.pack(pady=10)

    def setup_add_data_tab(self):
        """Форма додавання даних"""
        frame = ctk.CTkFrame(self.tabview.tab("Додати дані"), fg_color="white", border_width=1)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Додати новий рейс", font=("Arial", 18, "bold")).pack(pady=10)
        
        ctk.CTkEntry(frame, placeholder_text="Номер потяга", width=300).pack(pady=10)
        ctk.CTkEntry(frame, placeholder_text="Станція відправлення", width=300).pack(pady=10)
        ctk.CTkEntry(frame, placeholder_text="Станція призначення", width=300).pack(pady=10)
        
        ctk.CTkButton(frame, text="Зберегти в базу", fg_color="#2ECC71", hover_color="#27AE60").pack(pady=20)

    def setup_edit_tab(self):
        """Редагування"""
        ctk.CTkLabel(self.tabview.tab("Редагування"), text="Виберіть запис", text_color="black").pack(pady=20)
        ctk.CTkComboBox(self.tabview.tab("Редагування"), values=["Рейс #1", "Рейс #2"], width=300).pack(pady=10)
        ctk.CTkButton(self.tabview.tab("Редагування"), text="Редагувати", fg_color="#3498DB").pack(pady=10)
        ctk.CTkButton(self.tabview.tab("Редагування"), text="Видалити", fg_color="#E74C3C").pack(pady=10)

    def setup_roles_tab(self):
        """Керування ролями """
        ctk.CTkLabel(self.tabview.tab("Ролі"), text="Керування доступом", font=("Arial", 18, "bold")).pack(pady=10)
        
        user_frame = ctk.CTkFrame(self.tabview.tab("Ролі"), fg_color="white", border_width=1)
        user_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(user_frame, text="andrii_data_eng", text_color="black").pack(side="left", padx=20)
        ctk.CTkSegmentedButton(user_frame, values=["User", "Admin", "Moderator"]).pack(side="right", padx=20, pady=10)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()