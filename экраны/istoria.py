from tkinter import *
from tkinter import ttk  # Для создания таблицы (Treeview)
from datetime import datetime
from pathlib import Path
import sqlite3
from tkinter import messagebox

class TransactionManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def fetch_transactions_by_user(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM Users WHERE username = ?', (username,))
        user_id = cursor.fetchone()

        if user_id:
            user_id = user_id[0]
            cursor.execute(''' 
                SELECT Transactions.TransactionID, Transactions.type, Transactions.amount, Transactions.date, Transactions.description,
                       IncomeCategories.name AS income_category, ExpenseCategories.name AS expense_category
                FROM Transactions
                LEFT JOIN IncomeCategories ON Transactions.IncomeCategoryID = IncomeCategories.id
                LEFT JOIN ExpenseCategories ON Transactions.ExpenseCategoryID = ExpenseCategories.id
                WHERE Transactions.UserID = ? 
                ORDER BY Transactions.date DESC, Transactions.TransactionID DESC
            ''', (user_id,))
            transactions = cursor.fetchall()
        else:
            transactions = []

        conn.close()
        return transactions

    def get_balance_from_user(self, username):
        """Получает текущий баланс пользователя из таблицы Users."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT balance FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return 0  # Если пользователя не найдено, возвращаем 0, чтобы избежать ошибок

    def calculate_balance(self, transactions, username):
        """
        Вычисляет баланс пользователя на момент каждой транзакции.
        """
        balance = self.get_balance_from_user(username)  # Текущий баланс пользователя из базы
        initial_balance = balance

        # Проходим по транзакциям в порядке от старых к новым
        for transaction in reversed(transactions):  # Переворачиваем порядок обратно
            amount = transaction[2]  # Сумма транзакции
            if transaction[1] == 'Income':  # Если доход, вычитаем из текущего баланса
                balance -= amount
            elif transaction[1] == 'Expense':  # Если расход, добавляем к текущему балансу
                balance += amount
        initial_balance -= balance
        return initial_balance


class HistoryFrame(Frame):
    def __init__(self, parent, assets_path, logged_in_user):
        super().__init__(parent)
        self.assets_path = assets_path
        self.user = logged_in_user

        # Передаем путь к базе данных и создаем экземпляр TransactionManager
        self.transaction_manager = TransactionManager(r'C:\Users\amiri\PycharmProjects\kursach\экраны\cointracker.db')
        self.current_balance1 = self.transaction_manager.get_balance_from_user(self.user) - self.transaction_manager.calculate_balance(self.transaction_manager.fetch_transactions_by_user(self.user), self.user)
        # Получаем транзакции для текущего пользователя
        self.transactions = self.transaction_manager.fetch_transactions_by_user(self.user)
        self.current_balance = self.transaction_manager.calculate_balance(self.transactions, self.user)


        self.setup_ui()

    def setup_ui(self):
        self.configure(bg="#C4E0A6")

        # Настройка стиля таблицы
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=30)  # Шрифт для ячеек
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))  # Шрифт для заголовков

        # Настроим Canvas, таблицу и другие элементы...
        self.canvas = Canvas(self, bg="#C4E0A6", height=637, width=762, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(-2.0, 123.0, 761.9999901050287, 125.99999999027409, fill="#000000", outline="")

        # Если нет транзакций
        if not self.transactions:
            label = Label(self, text="Нет транзакций для данного пользователя", font=("Arial", 22), bg="#C4E0A6",
                          fg="#FF0000")
            label.place(x=100, y=200)
            return

        self.columns = ("ID", "Тип", "Категория", "Сумма", "Дата", "Время", "Описание")
        self.transactions_table = ttk.Treeview(self, columns=self.columns, show="headings", height=20)
        # Настроим столбцы таблицы Treeview
        self.transactions_table.heading("ID", text="ID")
        self.transactions_table.heading("Тип", text="Тип")
        self.transactions_table.heading("Категория", text="Категория")
        self.transactions_table.heading("Сумма", text="Сумма")
        self.transactions_table.heading("Дата", text="Дата")
        self.transactions_table.heading("Время", text="Время")
        self.transactions_table.heading("Описание", text="Описание")

        # Задаем ширину и выравнивание
        self.transactions_table.column("ID", width=0, stretch=False)
        self.transactions_table.column("Тип", width=50, anchor="center")
        self.transactions_table.column("Категория", width=50, anchor="center")
        self.transactions_table.column("Сумма", width=50, anchor="center")
        self.transactions_table.column("Дата", width=50, anchor="center")
        self.transactions_table.column("Время", width=50, anchor="center")
        self.transactions_table.column("Описание", width=0, stretch=False)  # Описание

        # Заполним таблицу транзакциями
        self.populate_transactions_table()

        self.transactions_table.place(x=10, y=130, width=740, height=425)

        # Добавление изображений и поля для баланса
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(196.0, 70.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(506.0, 569.0, image=self.image_image_2)

        self.TypeTransaction = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(418.0, 17.0, image=self.TypeTransaction)

        self.Summa = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(399.0, 75.0, image=self.Summa)

        self.Date = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_5 = self.canvas.create_image(526.0, 17.0, image=self.Date)

        expense_label = Label(self, text="Категория", font=("Century Gothic", 12), bg="#C4E0A6")
        expense_label.place(x=510, y=58)

        self.entry_image_balanse = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(534, 601.5, image=self.entry_image_balanse)
        self.balanse = Entry(self, bd=0, bg="#74C38C", fg="#000716", highlightthickness=0, font=("Arial", 14))
        self.balanse.place(x=490.0, y=585.0, width=100, height=35.0)
        self.balanse.config(state='readonly', readonlybackground="#74C38C")

        self.entry_image_Summa = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(422.5, 100.0, image=self.entry_image_Summa)
        self.Summa_entry = Entry(self, bd=0, bg="#68B980", fg="#000716", highlightthickness=0, font=("Arial", 12))
        self.Summa_entry.place(x=384.0, y=85.0, width=77.0, height=28.0)

        self.entry_image_Data = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(558.5, 42.0, image=self.entry_image_Data)
        self.Data = Entry(self, bd=0, bg="#68B980", fg="#000716", highlightthickness=0, font=("Arial", 12))
        self.Data.place(x=520.0, y=27.0, width=80.0, height=28.0)

        self.entry_image_Category = PhotoImage(file=self.relative_to_assets("entry_4.png"))
        self.entry_bg_4 = self.canvas.create_image(558.5, 100.0, image=self.entry_image_Category)
        self.Category_entry = Entry(self, bd=0, bg="#68B980", fg="#000716", highlightthickness=0, font=("Arial", 12))
        self.Category_entry.place(x=520.0, y=85.0, width=77.0, height=28.0)

        self.entry_image_TypeTransactionEntry = PhotoImage(file=self.relative_to_assets("entry_5.png"))
        self.entry_bg_5 = self.canvas.create_image(422.5, 42.0, image=self.entry_image_TypeTransactionEntry)
        self.TypeTransactionEntry = Entry(self, bd=0, bg="#68B980", fg="#000716", highlightthickness=0, font=("Arial", 12))
        self.TypeTransactionEntry.place(x=384.0, y=27.0, width=77.0, height=28.0)


        self.update_balance()

        # Добавление кнопок
        button_image_1 = self.load_image("button_1.png")
        button_1 = Button(
            self,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_transaction,
            relief="flat"
        )
        button_1.image = button_image_1  # Сохраняем ссылку на изображение
        button_1.place(x=608.0, y=570.0, width=61.0, height=57.0)

        button_image_2 = self.load_image("button_2.png")
        button_2 = Button(
            self,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.repeat_transaction,
            relief="flat"
        )
        button_2.image = button_image_2  # Сохраняем ссылку на изображение
        button_2.place(x=678.0, y=569.0, width=61.0, height=57.0)

        button_image_3 = self.load_image("button_3.png")
        button_3 = Button(
            self,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.apply_filters,
            relief="flat"
        )
        button_3.image = button_image_3  # Сохраняем ссылку на изображение
        button_3.place(x=632.0, y=38.0, width=118.0, height=69.0)




        # Создание подсказки
        self.tooltip_label = ttk.Label(self, text="", background="#C4E0A6", font=("Arial", 12))
        self.tooltip_label.place(x=10, y=580)

        # Настройка событий для подсказки
        self.transactions_table.bind("<Motion>", self.on_hover)
        self.transactions_table.bind("<Leave>", self.on_leave)

    def load_image(self, path: str):
        full_path = self.relative_to_assets(path)
        try:
            image = PhotoImage(file=full_path)
        except TclError:
            print(f"Ошибка загрузки изображения: {full_path}")
            image = PhotoImage()  # Возвращаем пустое изображение или заглушку
        return image

    def relative_to_assets(self, path: str) -> Path:
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame istoria")
        full_path = ASSETS_PATH / Path(path)
        return full_path

    def on_hover(self, event):
        item = self.transactions_table.identify_row(event.y)
        if item:
            values = self.transactions_table.item(item, "values")
            description = values[6]  # Столбец описания
            transaction_id = int(values[0])

            # Определяем индекс текущей транзакции
            for index, transaction in enumerate(self.transactions):
                if transaction[0] == transaction_id:
                    # Рассчитываем баланс до текущей транзакции
                    reversed_transactions = list(reversed(self.transactions[index:]))  # От текущей транзакции к старым
                    balance = self.transaction_manager.calculate_balance(reversed_transactions, self.user)

                    # Отображаем в подсказке
                    self.tooltip_label.config(
                        text=f"Описание: {description}\nБаланс после операции: {balance + self.current_balance1}",
                        font=("Arial", 14)  # Установите нужный шрифт и размер
                    )
                    break
        else:
            self.tooltip_label.config(text="")

    def on_leave(self, event):
        self.tooltip_label.config(text="")

    def format_datetime(self, datetime_str):
        # Попробуем сначала интерпретировать как полный datetime (с временем)
        try:
            dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Если не получилось, предположим, что время не указано
            dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d")

        date = dt_obj.strftime("%d.%m.%Y")
        time = dt_obj.strftime("%H:%M:%S") if len(
            datetime_str) > 10 else "00:00:00"  # Если время отсутствует, используем 00:00:00
        return date, time

    def translate_type(self, transaction_type):
        if transaction_type == 'Income':
            return 'Доход'
        elif transaction_type == 'Expense':
            return 'Расход'
        return transaction_type

    def update_balance(self):
        """Обновляет поле с балансом."""
        self.balanse.config(state='normal')
        self.balanse.delete(0, 'end')
        self.balanse.insert(0, str(self.current_balance + self.current_balance1))
        self.balanse.config(state='readonly', readonlybackground="#74C38C")


    def delete_transaction(self):
        selected_item = self.transactions_table.selection()
        if selected_item:
            item = self.transactions_table.item(selected_item)
            transaction_id = item["values"][0]
            print(f"Удаляем транзакцию с ID: {transaction_id}")

            # Подключаемся к базе данных
            conn = sqlite3.connect(self.transaction_manager.db_path)
            cursor = conn.cursor()

            # Удаляем транзакцию из базы данных
            cursor.execute('DELETE FROM Transactions WHERE TransactionID = ?', (transaction_id,))
            conn.commit()
            conn.close()

            # Обновляем транзакции и таблицу
            self.transactions = self.transaction_manager.fetch_transactions_by_user(self.user)
            self.populate_transactions_table()


    def repeat_transaction(self):
        selected_item = self.transactions_table.selection()
        if selected_item:
            item = self.transactions_table.item(selected_item)
            transaction_id = item["values"][0]
            print(f"Повторяем транзакцию с ID: {transaction_id}")

            # Подключаемся к базе данных
            conn = sqlite3.connect(self.transaction_manager.db_path)
            cursor = conn.cursor()

            try:
                # Получаем данные выбранной транзакции
                cursor.execute(''' 
                    SELECT type, amount, description, IncomeCategoryID, ExpenseCategoryID 
                    FROM Transactions 
                    WHERE TransactionID = ?
                ''', (transaction_id,))
                transaction_data = cursor.fetchone()

                if transaction_data:
                    transaction_type, amount, description, income_category_id, expense_category_id = transaction_data

                    # Получаем UserID для текущего пользователя
                    cursor.execute("SELECT id FROM Users WHERE username = ?", (self.user,))
                    user_id = cursor.fetchone()

                    if user_id:
                        user_id = user_id[0]

                        # Вставляем повторную транзакцию с автоматической датой и временем
                        cursor.execute(''' 
                            INSERT INTO Transactions (UserID, type, amount, date, description, IncomeCategoryID, ExpenseCategoryID)
                            VALUES (?, ?, ?, strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'), ?, ?, ?)
                        ''', (user_id, transaction_type, amount, description, income_category_id, expense_category_id))
                        conn.commit()

                        print("Транзакция повторена успешно.")
                    else:
                        print(f"Пользователь с именем {self.user} не найден в базе данных.")

                else:
                    print(f"Транзакция с ID {transaction_id} не найдена.")

            except sqlite3.Error as e:
                print(f"Ошибка базы данных: {e}")

            finally:
                conn.close()

            # Обновляем транзакции и таблицу
            self.transactions = self.transaction_manager.fetch_transactions_by_user(self.user)
            self.populate_transactions_table()

    def populate_transactions_table(self):
        self.transactions_table.delete(*self.transactions_table.get_children())

        for transaction in self.transactions:
            transaction_id = transaction[0]
            transaction_type = self.translate_type(transaction[1])
            amount = transaction[2]
            if transaction_type == 'Расход':
                amount = -amount
            date, time = self.format_datetime(transaction[3])
            description = transaction[4]
            income_category = transaction[5] if transaction[5] else "Без категории"
            expense_category = transaction[6] if transaction[6] else "Без категории"

            self.transactions_table.insert("", "end", values=(
                transaction_id,
                transaction_type,
                income_category if transaction_type == 'Доход' else expense_category,
                amount,
                date,
                time,
                description
            ))

    def apply_filters(self):
        transaction_type = self.TypeTransactionEntry.get().strip().lower()
        category = self.Category_entry.get().strip().lower()
        amount = self.Summa_entry.get().strip()
        date = self.Data.get().strip()

        if not hasattr(self, 'all_transactions'):
            self.all_transactions = self.transactions[:]

        if not (transaction_type or category or amount or date):
            self.transactions = self.all_transactions[:]
            self.populate_transactions_table()
            return

        if transaction_type and transaction_type not in ['доход', 'расход']:
            messagebox.showerror("Ошибка", "Некорректный тип транзакции. Используйте 'Доход' или 'Расход'.")
            return

        filtered_transactions = self.all_transactions

        if transaction_type:
            db_type = 'Income' if transaction_type == 'доход' else 'Expense'
            filtered_transactions = [t for t in filtered_transactions if t[1].lower() == db_type.lower()]

        if category:
            if not transaction_type:
                messagebox.showerror("Ошибка", "Заполните поле 'Тип транзакции' перед выбором категории.")
                return

            category_index = 5 if db_type == 'Income' else 6
            filtered_transactions = [t for t in filtered_transactions if
                                     t[category_index] and t[category_index].lower() == category]

        if amount:
            try:
                amount = float(amount)
                filtered_transactions = [t for t in filtered_transactions if t[2] == amount]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректное значение суммы.")
                return

        if date:
            try:
                date_obj = datetime.strptime(date, "%d.%m.%Y")
                filtered_transactions = [t for t in filtered_transactions if
                                         t[3].startswith(date_obj.strftime("%Y-%m-%d"))]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте DD.MM.YYYY.")
                return

        self.transactions = filtered_transactions
        self.populate_transactions_table()



