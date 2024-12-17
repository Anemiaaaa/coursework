import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import sqlite3


class DatabaseManager:
    """Класс для работы с базой данных."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def check_user_credentials(self, username: str, password: str) -> bool:
        """Проверяет корректность логина и пароля."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Предполагаем, что таблица пользователей теперь имеет UserID, username и password
        cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
        result = cursor.fetchone()
        conn.close()

        return result is not None


class AuthorizationApp:
    """Класс для управления окном авторизации."""

    def __init__(self, root: Tk, db_manager: DatabaseManager):
        self.root = root
        self.db_manager = db_manager
        self.logged_in_user = None

        self.setup_ui()

    def setup_ui(self):
        """Настраивает пользовательский интерфейс."""
        self.root.geometry("1093x637")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        self.root.bind('<Return>', self.check_credentials)

        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=637,
            width=1093,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # UI Elements
        self.canvas.create_rectangle(0, 0, 721, 637, fill="#C4E0A6", outline="")
        self.canvas.create_rectangle(711, 0, 721, 1189, fill="#74C38C", outline="")

        self.entry_1 = self.create_entry(910, 212.5, "entry_1.png", False)
        self.entry_2 = self.create_entry(910.5, 361.5, "entry_2.png", True)

        self.canvas.create_text(782, 308, anchor="nw", text="Password\n", fill="#000000", font=("Inter SemiBold", -20))
        self.canvas.create_text(782, 160, anchor="nw", text="Login", fill="#000000", font=("Inter SemiBold", -20))

        self.create_button(819, 451, 182.086, 51, "button_1.png", self.check_credentials)
        self.create_button(917, 583, 160, 35, "button_3.png", self.open_registration)

        self.add_image(320, 296, "image_1.png")
        self.add_image(909, 114, "image_2.png")
        self.add_image(150, 485, "image_3.png")
        self.add_image(599, 520, "image_4.png")
        self.add_image(591, 123, "image_5.png")
        self.add_image(397, 477, "image_6.png")
        self.add_image(125, 141, "image_7.png")
        self.add_image(638, 357, "image_8.png")
        self.add_image(339, 113, "image_9.png")

    def create_entry(self, x, y, img_file, is_password):
        """Создает текстовое поле."""
        entry_image = PhotoImage(file=self.relative_to_assets(img_file))
        self.canvas.create_image(x, y, image=entry_image)
        entry = Entry(
            bd=0,
            bg="#74C38C" if not is_password else "#73C38B",
            fg="#000716",
            highlightthickness=0,
            font=("Arial", 16),
            show="*" if is_password else ""
        )
        entry.place(x=x - 130.5, y=y - 17.5, width=261, height=40)
        entry.image = entry_image  # Чтобы избежать удаления изображения
        return entry

    def create_button(self, x, y, width, height, img_file, command):
        """Создает кнопку."""
        button_image = PhotoImage(file=self.relative_to_assets(img_file))
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button.place(x=x, y=y, width=width, height=height)
        button.image = button_image  # Чтобы избежать удаления изображения
        return button

    def add_image(self, x, y, img_file):
        """Добавляет изображение."""
        image = PhotoImage(file=self.relative_to_assets(img_file))
        self.canvas.create_image(x, y, image=image)
        image.image = image  # Чтобы избежать удаления изображения

    @staticmethod
    def relative_to_assets(path: str) -> Path:
        """Возвращает относительный путь к файлу."""
        return Path(__file__).parent / Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame autorizacia") / Path(
            path)

    def check_credentials(self, event=None):
        """Проверяет учетные данные пользователя."""
        username = self.entry_1.get()
        password = self.entry_2.get()

        if self.db_manager.check_user_credentials(username, password):
            self.logged_in_user = username
            self.open_main()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def open_main(self):
        """Открывает главное окно."""
        if self.logged_in_user:
            self.root.withdraw()  # Скрыть текущее окно
            subprocess.Popen(["python", "main.py", self.logged_in_user])  # Запуск нового процесса
        else:
            messagebox.showerror("Ошибка", "Вы не вошли в систему")

    def open_registration(self):
        """Открывает окно регистрации."""
        subprocess.Popen(["python", "register.py"])


if __name__ == "__main__":
    # Обновляем путь к базе данных в соответствии с новой структурой
    database_manager = DatabaseManager("cointracker.db")
    root = Tk()
    app = AuthorizationApp(root, database_manager)
    root.mainloop()

