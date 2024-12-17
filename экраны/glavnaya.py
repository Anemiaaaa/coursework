import subprocess
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Frame, Listbox, Label
import sys
from pathlib import Path
import sqlite3

sys.path.append(str(Path(__file__).resolve().parent.parent))
from экраны.istoria import TransactionManager


class Application(Frame):
    def __init__(self, frame, assets_path, logged_in_user):
        super().__init__(frame)
        self.frame = frame
        self.assets_path = assets_path
        self.logged_in_user = logged_in_user
        self.transaction_manager = TransactionManager(r'C:\Users\amiri\PycharmProjects\kursach\экраны\cointracker.db')
        self.category_analytics = CategoryAnalytics(r'C:\Users\amiri\PycharmProjects\kursach\экраны\cointracker.db')
        self.current_balance = self.transaction_manager.calculate_balance(
            self.transaction_manager.fetch_transactions_by_user(self.logged_in_user),
            self.logged_in_user
        )
        self.setup_window()
        self.setup_canvas()

        self.setup_buttons()
        self.setup_entries()
        self.setup_images()
        self.setup_lists()  # Setup lists for top categories
        self.update_balance_entry()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_window(self):
        self.frame.configure(bg="#C4E0A6")

    def open_RashodCategory_window(self):
        subprocess.Popen(
            ["python", r"C:\\Users\\amiri\\PycharmProjects\\kursach\\экраны\\RashodCategory.py", self.logged_in_user]
        )

    def open_DohodCategory_window(self):
        subprocess.Popen(
            ["python", r"C:\\Users\\amiri\\PycharmProjects\\kursach\\экраны\\DohodCategory.py", self.logged_in_user]
        )

    def setup_canvas(self):
        self.canvas = Canvas(
            self.frame,
            bg="#C4E0A6",
            height=637,
            width=762,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

    def setup_buttons(self):
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.frame,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_RashodCategory_window,
            relief="flat"
        )
        self.button_1.place(x=43.0, y=263.0, width=302.0, height=85.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.frame,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_DohodCategory_window,
            relief="flat"
        )
        self.button_2.place(x=419.0, y=263.0, width=302.0, height=85.0)

    def setup_entries(self):
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(388.0, 182.0, image=self.entry_image_1)
        self.entry_1 = Entry(
            self.frame,
            bd=0,
            bg="#74C38C",
            fg="#000716",
            highlightthickness=0,
            font=("Arial", 22),
            justify='center'
        )
        self.entry_1.config(state='readonly', readonlybackground="#74C38C")
        self.entry_1.place(x=298.0, y=158.0, width=180.0, height=46.0)

    def setup_images(self):
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(193.0, 70.0, image=self.image_image_1)

        self.canvas.create_rectangle(
            -2.0,
            123.0,
            761.9999901050287,
            125.99999999027409,
            fill="#000000",
            outline=""
        )

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(161.0, 180.0, image=self.image_image_2)

    def setup_lists(self):
        # Labels for the lists with Century Gothic font
        income_label = Label(self.frame, text="Топ категорий дохода", bg="#C4E0A6", font=("Century Gothic", 20))
        income_label.place(x=30, y=365)

        expense_label = Label(self.frame, text="Топ категорий расхода", bg="#C4E0A6",
                              font=("Century Gothic", 20))
        expense_label.place(x=410, y=365)

        # Listboxes for categories with Century Gothic font, background color #74C38C, borders, and custom selection color
        self.income_list = Listbox(self.frame, height=5, width=20, font=("Century Gothic", 18), bg="#74C38C",
                                   fg="black", selectbackground="lightgreen", bd=10, relief="raised")
        self.income_list.place(x=50, y=420)

        self.expense_list = Listbox(self.frame, height=5, width=20, font=("Century Gothic", 18), bg="#74C38C",
                                    fg="black", selectbackground="lightgreen", bd=10, relief="raised")
        self.expense_list.place(x=450, y=420)

        # Populate the lists with top categories
        self.populate_top_categories()

    def get_balance_from_user(self, username):
        """Получает текущий баланс пользователя из таблицы Users."""
        conn = sqlite3.connect(self.transaction_manager.db_path)  # Используем db_path из TransactionManager
        cursor = conn.cursor()

        cursor.execute('SELECT balance FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]  # Возвращаем баланс
        else:
            return None  # Если пользователь не найден

    def populate_top_categories(self):
        # Fetch and display top categories
        try:
            top_expenses = self.category_analytics.get_top_categories(self.logged_in_user, "Expense")
            if not top_expenses:
                print("No expense categories found")
            for name, total in top_expenses:
                self.expense_list.insert("end", f"{name}: {total}")

            top_incomes = self.category_analytics.get_top_categories(self.logged_in_user, "Income")
            if not top_incomes:
                print("No income categories found")
            for name, total in top_incomes:
                self.income_list.insert("end", f"{name}: {total}")

        except Exception as e:
            print(f"Error while populating categories: {e}")

    def update_balance_entry(self):
        self.entry_1.config(state='normal')
        self.entry_1.delete(0, 'end')
        self.entry_1.insert(0, str(self.get_balance_from_user(self.logged_in_user)))
        self.entry_1.config(state='readonly', readonlybackground="#74C38C")


class CategoryAnalytics:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_user_id(self, username):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM Users WHERE username = ?', (username,))
                user_id = cursor.fetchone()
                if user_id:
                    return user_id[0]
                else:
                    return None
        except Exception as e:
            print(f"Error fetching user ID: {e}")
            return None

    def get_top_categories(self, username, category_type):
        user_id = self.get_user_id(username)
        if user_id is None:
            print(f"No user found with username: {username}")
            return []

        query = ""
        if category_type == "Expense":
            query = """
                WITH ExpenseData AS (
                    SELECT ec.name AS category_name, SUM(t.Amount) AS total,
                           ROW_NUMBER() OVER (ORDER BY SUM(t.Amount) DESC) AS row_num
                    FROM Transactions t
                    LEFT JOIN ExpenseCategories ec ON t.ExpenseCategoryID = ec.id
                    WHERE t.UserID = ?
                    GROUP BY ec.name
                    HAVING ec.name IS NOT NULL
                )
                SELECT category_name, total FROM ExpenseData
                WHERE row_num <= 3
                ORDER BY total DESC
            """
        elif category_type == "Income":
            query = """
                WITH IncomeData AS (
                    SELECT ic.name AS category_name, SUM(t.Amount) AS total,
                           ROW_NUMBER() OVER (ORDER BY SUM(t.Amount) DESC) AS row_num
                    FROM Transactions t
                    LEFT JOIN IncomeCategories ic ON t.IncomeCategoryID = ic.id
                    WHERE t.UserID = ?
                    GROUP BY ic.name
                    HAVING ic.name IS NOT NULL
                )
                SELECT category_name, total FROM IncomeData
                WHERE row_num <= 3
                ORDER BY total DESC
            """

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (user_id,))
                results = cursor.fetchall()
                print(f"Query results for {category_type}: {results}")
                return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

