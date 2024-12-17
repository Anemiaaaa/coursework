import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from tkinter import messagebox  # Импортируем messagebox


class Application:
    def __init__(self, root):
        self.root = root
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame register")
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_ui(self):
        self.root.geometry("955x463")
        self.root.configure(bg="#C4E0A6")

        self.canvas = Canvas(
            self.root,
            bg="#C4E0A6",
            height=463,
            width=955,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(529.0, 0.0, 955.0, 463.0, fill="#74C38C", outline="")

        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(745.5, 328, image=self.entry_image_1)
        self.entry_1 = Entry(bd=0, bg="#8BDEA5", fg="#000716", highlightthickness=0, font=("Arial", 16))
        self.entry_1.place(x=615.0, y=308.0, width=261.0, height=41.0)

        self.canvas.create_text(607.0, 276.0, anchor="nw", text="Начальный баланс", fill="#000000", font=("Inter SemiBold", 18 * -1))

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(741.5, 133, image=self.entry_image_2)
        self.entry_2 = Entry(bd=0, bg="#8BDEA5", fg="#000716", highlightthickness=0, font=("Arial", 16))
        self.entry_2.place(x=611.0, y=113.0, width=261.0, height=41.0)

        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(745.5, 232, image=self.entry_image_3)
        self.entry_3 = Entry(bd=0, bg="#8BDEA5", fg="#000716", highlightthickness=0, font=("Arial", 16))
        self.entry_3.place(x=615.0, y=211.0, width=261.0, height=41.0)

        self.canvas.create_text(613.0, 83.0, anchor="nw", text="Логин", fill="#000000", font=("Inter SemiBold", 18 * -1))

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(241.0, 225.0, image=self.image_image_1)

        self.canvas.create_text(613.0, 178.0, anchor="nw", text="Пароль", fill="#000000", font=("Inter SemiBold", 18 * -1))

        self.canvas.create_text(644.0, 24.0, anchor="nw", text="Регистрация", fill="#000000", font=("Inter SemiBold", 30 * -1))

        self.canvas.create_rectangle(526.0, -3.0, 529.0, 463.0, fill="#000000", outline="")

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_register_button_click,  # Привязываем обработчик
            relief="flat"
        )
        self.button_1.place(x=648.0, y=381.0, width=188.0, height=42.0)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(267.0208740234375, 247.0, image=self.image_image_2)

        self.root.resizable(False, False)

    def add_user_to_db(self, username, password, balance):
        # Подключение к базе данных
        db_path = r'C:\Users\amiri\PycharmProjects\kursach\экраны\cointracker.db'  # Укажите путь к вашей базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Проверим, существует ли уже пользователь с таким логином
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует.")
            conn.close()
            return

        # Добавляем нового пользователя в базу данных
        cursor.execute(
            "INSERT INTO Users (username, password, balance) VALUES (?, ?, ?)",
            (username, password, balance)
        )

        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", f"Пользователь {username} успешно добавлен.")

    def on_register_button_click(self):
        username = self.entry_2.get()
        password = self.entry_3.get()
        balance = self.entry_1.get()

        # Проверка на пустые поля
        if not username or not password or not balance:
            messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены.")
            return

        try:
            balance = float(balance)  # Конвертируем баланс в число
        except ValueError:
            messagebox.showerror("Ошибка", "Баланс должен быть числом.")
            return

        # Добавление пользователя в базу данных
        self.add_user_to_db(username, password, balance)
        self.root.iconify() # Свернем окно регистрации

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
