from pathlib import Path
from tkinter import Frame, Canvas, Button, PhotoImage, Toplevel, Label
import sqlite3
import subprocess

class Categories(Frame):
    def __init__(self, parent_frame, assets_path, username):
        super().__init__(parent_frame)  # Bind to the parent frame
        self.assets_path = assets_path
        self.username = username
        self.Type = "Income"
        self.Type1 = "Expense"
        print(f"Initialized with Type: {self.Type}, Type1: {self.Type1}")  # Debugging
        self.setup_canvas()
        self.setup_widgets()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_canvas(self):
        self.canvas = Canvas(
            self,
            bg="#C4E0A6",
            height=637,
            width=762,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            -2.0,
            123.0,
            761.9999901050287,
            125.99999999027409,
            fill="#000000",
            outline=""
        )
        self.canvas.create_rectangle(
            1.0,
            375.0,
            764.9999901050287,
            377.9999999902741,
            fill="#000000",
            outline=""
        )

    def setup_widgets(self):
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(231.0, 71.0, image=self.image_image_1)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(152.0, 500.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(154.0, 256.0, image=self.image_image_4)

        self.create_buttons()

    def create_buttons(self):
        button_images = [
            "button_1.png", "button_2.png", "button_3.png", "button_4.png",
            "button_5.png", "button_6.png", "button_7.png", "button_8.png",
            "button_9.png", "button_10.png", "button_11.png", "button_12.png"
        ]

        button_positions = [
            (629.0, 516.0), (489.0, 516.0), (349.0, 516.0), (629.0, 408.0),
            (489.0, 408.0), (349.0, 408.0), (629.0, 253.0), (489.0, 253.0),
            (349.0, 253.0), (629.0, 145.0), (489.0, 145.0), (349.0, 145.0)
        ]

        button_category = [
            6, 5, 4, 3, 1, 2, 6, 5, 4, 3, 2, 1
        ]

        button_type = [self.Type] * 6 + [self.Type1] * 6
        print(f"Button type list: {button_type}")  # Debugging to see if this list is generated correctly

        for image, position, category, type in zip(button_images, button_positions, button_category, button_type):
            button_image = PhotoImage(file=self.relative_to_assets(image))
            button = Button(
                self,  # Binding to the current Frame
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=lambda cat=category, usr=self.username, tp=type: self.open_summ_opisanie_window(cat, usr, tp),
                relief="flat"
            )
            button.image = button_image  # Keeping a reference to the image
            button.place(x=position[0], y=position[1], width=86.0, height=89.0)

            # Добавление всплывающей подсказки
            Tooltip(button, lambda cat=category, tp=type: self.get_tooltip_text(cat, tp))

    def get_tooltip_text(self, category, transaction_type):
        """Получить текст подсказки о количестве транзакций и сумме из базы данных для конкретного пользователя."""
        db_path = r'C:\\Users\\amiri\\PycharmProjects\\kursach\\экраны\\cointracker.db'

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Получение идентификатора пользователя из имени пользователя
            cursor.execute('SELECT id FROM Users WHERE username = ?', (self.username,))
            user_id = cursor.fetchone()
            if not user_id:
                conn.close()
                return "Пользователь не найден"
            user_id = user_id[0]

            if transaction_type == "Income":
                cursor.execute('''
                    SELECT COUNT(*), COALESCE(SUM(Amount), 0)
                    FROM Transactions
                    WHERE IncomeCategoryID = ? AND Type = 'Income' AND UserID = ?
                ''', (category, user_id))
                result = cursor.fetchone()

                cursor.execute('SELECT name FROM IncomeCategories WHERE id = ?', (category,))
                category_name = cursor.fetchone()
            elif transaction_type == "Expense":
                cursor.execute('''
                    SELECT COUNT(*), COALESCE(SUM(Amount), 0)
                    FROM Transactions
                    WHERE ExpenseCategoryID = ? AND Type = 'Expense' AND UserID = ?
                ''', (category, user_id))
                result = cursor.fetchone()

                cursor.execute('SELECT name FROM ExpenseCategories WHERE id = ?', (category,))
                category_name = cursor.fetchone()
            else:
                return "Неизвестный тип транзакции"

            # Проверка результатов
            transaction_count = result[0] if result else 0
            total_sum = result[1] if result else 0.0

            category_name = category_name[0] if category_name else "Неизвестная категория"

            conn.close()

            return f"Транзакций: {transaction_count}\nСумма: {total_sum} руб."

        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")
            return "Ошибка загрузки данных"

    def open_summ_opisanie_window(self, category, logged_in_user, Type):
        subprocess.Popen(["python", r"C:\\Users\\amiri\\PycharmProjects\\kursach\\экраны\\SummaOpisanie.py", str(category), logged_in_user, Type])

# Tooltip класс для отображения всплывающей информации
class Tooltip:
    """Класс для создания всплывающих подсказок."""

    def __init__(self, widget, text_provider):
        self.widget = widget
        self.text_provider = text_provider
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        """Показать подсказку при наведении мыши."""
        if self.tooltip_window:
            return  # Если окно уже открыто, не создавать новое

        # Получаем текст подсказки
        text = self.text_provider()

        # Создаем окно подсказки
        self.tooltip_window = Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Убираем рамки окна
        self.tooltip_window.configure(bg="#000000", padx=2, pady=2)  # Белый фон и отступы

        # Позиционируем окно рядом с курсором
        x = self.widget.winfo_rootx() + event.x + 10
        y = self.widget.winfo_rooty() + event.y + 10
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Создаем текстовую метку
        label = Label(
            self.tooltip_window,
            text=text,
            justify="left",
            bg="#8CDFA5",  # Белый фон
            relief="flat",  # Рамка вокруг текста

            font=("Century Gothic", 12)  # Увеличенный шрифт
        )
        label.pack()

    def hide_tooltip(self, event):
        """Скрыть подсказку при выходе мыши."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

