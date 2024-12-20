import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path
from tkinter import Frame, Canvas, PhotoImage, Radiobutton, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
from tkinter import Button, PhotoImage, TclError
from tkinter import Label, Toplevel
from tkcalendar import DateEntry
from tkinter import Button


class Obshiy(Frame):
    def __init__(self, parent, assets_path, username):
        super().__init__(parent)
        self.frame = parent
        self.assets_path = assets_path
        self.logged_in_user = username
        self.period = StringVar(value="day")  # Переменная для выбора периода
        self.start_date = StringVar()  # Начальная дата для пользовательского периода
        self.end_date = StringVar()  # Конечная дата для пользовательского периода
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_ui(self):
        """Настройка интерфейса и отображение графика"""
        self.canvas = Canvas(
            self.frame,
            bg="#74C38C",
            height=800,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Кнопки для выбора периода
        button_image_week = self.load_image("button_1.png")
        button_1 = Button(
            self.frame,
            image=button_image_week,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.change_period("week"),
            relief="flat"
        )
        button_1.image = button_image_week  # Сохраняем ссылку на изображение
        button_1.place(
            x=282.0,
            y=3.0,
            width=140.0,
            height=37.0
        )

        button_image_year = self.load_image("button_2.png")
        button_2 = Button(
            self.frame,
            image=button_image_year,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.change_period("year"),
            relief="flat"
        )
        button_2.image = button_image_year  # Сохраняем ссылку на изображение
        button_2.place(
            x=2.0,
            y=3.0,
            width=140.0,
            height=37.0
        )

        button_image_month = self.load_image("button_3.png")
        button_3 = Button(
            self.frame,
            image=button_image_month,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.change_period("month"),
            relief="flat"
        )
        button_3.image = button_image_month  # Сохраняем ссылку на изображение
        button_3.place(
            x=142.0,
            y=3.0,
            width=140.0,
            height=37.0
        )

        button_image_day = self.load_image("button_4.png")
        button_4 = Button(
            self.frame,
            image=button_image_day,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.change_period("day"),
            relief="flat"
        )
        button_4.image = button_image_day  # Сохраняем ссылку на изображение
        button_4.place(
            x=422.0,
            y=3.0,
            width=140.0,
            height=37.0
        )

        button_image_custom = self.load_image("button_5.png")
        button_5 = Button(
            self.frame,
            image=button_image_custom,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_custom_period_window,
            relief="flat"
        )
        button_5.image = button_image_custom  # Сохраняем ссылку на изображение
        button_5.place(
            x=562.0,
            y=3.0,
            width=140.0,
            height=37.0
        )

        # Генерация данных и создание графика
        self.times, self.incomes, self.expenses, self.data = self.generate_data_from_db()
        self.create_graph()

    def open_custom_period_window(self):
        """Открывает новое окно для ввода периода"""
        custom_window = Toplevel(self.frame)
        custom_window.title("Выберите свой период")
        custom_window.geometry("300x200")
        custom_window.configure(bg="#F0F0F0")

        # Метки и поля для ввода дат
        start_date_label = Label(custom_window, text="Начальная дата (yyyy-mm-dd):", bg="#F0F0F0", fg="#333333",
                                 font=("Arial", 10))
        start_date_label.pack(pady=5)
        self.start_date_entry = DateEntry(custom_window, date_pattern='yyyy-mm-dd', background='#FFFFFF',
                                          foreground='#000000', borderwidth=2)
        self.start_date_entry.pack(pady=5)

        end_date_label = Label(custom_window, text="Конечная дата (yyyy-mm-dd):", bg="#F0F0F0", fg="#333333",
                               font=("Arial", 10))
        end_date_label.pack(pady=5)
        self.end_date_entry = DateEntry(custom_window, date_pattern='yyyy-mm-dd', background='#FFFFFF',
                                        foreground='#000000', borderwidth=2)
        self.end_date_entry.pack(pady=5)

        # Кнопка для подтверждения ввода
        confirm_button = Button(
            custom_window,
            text="Применить",
            command=lambda: self.apply_custom_period(custom_window),
            relief="flat",
            bg="#4CAF50",
            fg="#FFFFFF",
            font=("Arial", 10, "bold")
        )
        confirm_button.pack(pady=10)

    def apply_custom_period(self, window):
        """Применяет выбранный период и обновляет график"""
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        if start_date and end_date:
            self.period.set("custom")
            self.update_graph_custom_period(start_date, end_date)

        # Закрываем окно после выбора периода
        window.destroy()

    def open_custom_period(self):
        """Обработчик для кнопки выбора пользовательского периода"""
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        if start_date and end_date:
            self.period.set("custom")
            self.update_graph_custom_period(start_date, end_date)

    def update_graph_custom_period(self, start_date, end_date):
        """Обновление графика для пользовательского периода"""
        self.times, self.incomes, self.expenses, self.data = self.generate_data_from_db_custom_period(start_date, end_date)
        self.create_graph()

    def generate_data_from_db_custom_period(self, start_date, end_date):
        """Получение данных из базы данных для графика в пределах пользовательского периода"""
        try:
            db_path = r'C:\Users\amiri\PycharmProjects\kursach\экраны\cointracker.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM Users WHERE username = ?', (self.logged_in_user,))
            user_id = cursor.fetchone()

            if not user_id:
                raise ValueError(f"User {self.logged_in_user} not found in the database.")

            query = '''
            SELECT Date, Type, Amount, Description, IncomeCategoryID, ExpenseCategoryID
            FROM Transactions
            WHERE UserID = ? AND Date BETWEEN ? AND ?
            '''
            cursor.execute(query, (user_id[0], start_date, end_date))
            transactions = cursor.fetchall()

            income_categories = {}
            expense_categories = {}
            cursor.execute('SELECT id, name FROM IncomeCategories')
            for row in cursor.fetchall():
                income_categories[row[0]] = row[1]
            cursor.execute('SELECT id, name FROM ExpenseCategories')
            for row in cursor.fetchall():
                expense_categories[row[0]] = row[1]

            # Группировка транзакций по дням
            times = {}
            for transaction in transactions:
                date_str = transaction[0]  # Используем полную дату как строку
                if date_str not in times:
                    times[date_str] = {'Income': 0, 'Expense': 0, 'Details': []}
                if transaction[1] == 'Income':  # Доходы
                    times[date_str]['Income'] += transaction[2]
                    category_name = income_categories.get(transaction[4], "Неизвестная категория")
                elif transaction[1] == 'Expense':  # Расходы
                    times[date_str]['Expense'] += transaction[2]
                    category_name = expense_categories.get(transaction[5], "Неизвестная категория")
                else:
                    continue
                times[date_str]['Details'].append(
                    (transaction[3], category_name, transaction[2], transaction[0], transaction[1]))

            # Сортируем по датам
            sorted_dates = sorted(times.keys())
            incomes = [times[date]['Income'] for date in sorted_dates]
            expenses = [times[date]['Expense'] for date in sorted_dates]

            conn.close()

            return sorted_dates, incomes, expenses, times

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")

        return [], [], [], {}

    def update_graph(self):
        self.times, self.incomes, self.expenses, self.data = self.generate_data_from_db()
        self.create_graph()

    def generate_data_from_db(self):
        """Получение данных из базы данных для графика (доходы, расходы, время)"""
        try:
            db_path = r'C:\Users\amiri\PycharmProjects\kursach\экраны\cointracker.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM Users WHERE username = ?', (self.logged_in_user,))
            user_id = cursor.fetchone()

            if not user_id:
                raise ValueError(f"User {self.logged_in_user} not found in the database.")

            query = '''
            SELECT Date, Type, Amount, Description, IncomeCategoryID, ExpenseCategoryID
            FROM Transactions
            WHERE UserID = ?
            '''
            cursor.execute(query, (user_id[0],))
            transactions = cursor.fetchall()

            income_categories = {}
            expense_categories = {}
            cursor.execute('SELECT id, name FROM IncomeCategories')
            for row in cursor.fetchall():
                income_categories[row[0]] = row[1]
            cursor.execute('SELECT id, name FROM ExpenseCategories')
            for row in cursor.fetchall():
                expense_categories[row[0]] = row[1]

            times = {}
            for transaction in transactions:
                time_str = self.get_time_period(transaction[0])
                if time_str is None:
                    continue

                if self.period.get() == "day":
                    # Для "дня" используем только часы и минуты
                    time_label = time_str.split()[1][:5]  # Формат HH:MM
                elif self.period.get() == "year":
                    # Для "года" используем только день и месяц
                    time_label = time_str.split()[0][5:10].replace("-", ".")  # Формат DD.MM
                else:
                    time_label = time_str

                if time_label not in times:
                    times[time_label] = {'Income': 0, 'Expense': 0, 'Details': []}

                if transaction[1] == 'Income':  # Доходы
                    times[time_label]['Income'] += transaction[2]
                    category_name = income_categories.get(transaction[4], "Неизвестная категория")
                elif transaction[1] == 'Expense':  # Расходы
                    times[time_label]['Expense'] += transaction[2]
                    category_name = expense_categories.get(transaction[5], "Неизвестная категория")
                else:
                    continue

                times[time_label]['Details'].append(
                    (transaction[3], category_name, transaction[2], transaction[0], transaction[1]))

            sorted_times = sorted(times.keys())
            incomes = [times[time]['Income'] for time in sorted_times]
            expenses = [times[time]['Expense'] for time in sorted_times]

            conn.close()

            return sorted_times, incomes, expenses, times

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")

        return [], [], [], {}

    def load_image(self, path: str):
        full_path = self.relative_to_assets(path)
        try:
            image = PhotoImage(file=full_path)
        except TclError:
            print(f"Ошибка загрузки изображения: {full_path}")
            image = PhotoImage()  # Возвращаем пустое изображение или заглушку
        return image

    def get_time_period(self, datetime_str):
        """Получаем строку для фильтрации по времени (день, неделя, месяц, год)"""
        import datetime
        date = datetime.datetime.strptime(datetime_str.split()[0], "%Y-%m-%d")
        today = datetime.datetime.now()

        if self.period.get() == "day":
            # Вернуть полную дату и время, если транзакция за сегодня
            if date.date() == today.date():
                return datetime_str  # Возвращаем полное время транзакции
            else:
                return None

        elif self.period.get() == "week":
            current_week = today.isocalendar()[1]
            transaction_week = date.isocalendar()[1]
            if date.year == today.year and transaction_week == current_week:
                return date.strftime("%Y-%m-%d")
            else:
                return None

        elif self.period.get() == "month":
            if date.year == today.year and date.month == today.month:
                return date.strftime("%Y-%m-%d")
            else:
                return None

        elif self.period.get() == "year":
            return date.strftime("%Y-%m-%d")
        else:
            return date.strftime("%Y-%m")

    def create_graph(self):
        """Создание улучшенного графика"""
        fig, ax = plt.subplots(figsize=(1, 1))  # Размеры графика

        bar_width = 0.4
        x = range(len(self.times))
        income_values = self.incomes
        expense_values = self.expenses

        # Столбцы доходов и расходов
        bars_income = ax.bar(x, income_values, bar_width, label='Доходы', color='#6ECF68', edgecolor='black',
                             linewidth=0.7)
        bars_expense = ax.bar([i + bar_width for i in x], expense_values, bar_width, label='Расходы', color='#FF6F61',
                              edgecolor='black', linewidth=0.7)

        # Настройка сетки
        ax.grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

        # Настройка осей
        ax.set_ylabel("Сумма", fontsize=10, labelpad=10, fontname="Century Gothic")

        # Легенда
        ax.legend(fontsize=8, loc='upper right', frameon=True, framealpha=0.9, edgecolor='gray')

        # Добавление численных значений поверх столбцов
        for bar in bars_income:
            yval = bar.get_height()
            if yval > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.0f}', ha='center', va='bottom',
                        fontsize=7, fontname="Century Gothic")
        for bar in bars_expense:
            yval = bar.get_height()
            if yval > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.0f}', ha='center', va='bottom',
                        fontsize=7, fontname="Century Gothic")

        # Вставка графика в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().place(x=5, y=50, width=690, height=320)
        canvas.draw()

        # Убираем подписи на оси X, если период "custom"
        if self.period.get() == "custom":
            ax.set_xticks([])  # Убираем все метки оси X
        else:
            ax.set_xticks([i + bar_width / 2 for i in x])
            ax.set_xticklabels(
                self.times,
                fontsize=8,
                rotation=0,  # Горизонтальная ориентация текста
                ha='center',
                fontname="Century Gothic"
            )

        # Добавление подсказок только если период НЕ "day"
        if self.period.get() != "day":
            self.add_tooltips(bars_income, bars_expense)

    def change_period(self, period):
        """Изменение периода фильтрации и обновление графика"""
        self.period.set(period)
        self.update_graph()

    def add_tooltips(self, bars_income, bars_expense):
        """Добавление подсказок при наведении на столбик"""
        cursor_income = mplcursors.cursor(bars_income, hover=True)
        cursor_expense = mplcursors.cursor(bars_expense, hover=True)

        # Подсказка для доходов
        @cursor_income.connect("add")
        def on_add_income(sel):
            index = sel.index
            date = self.times[index]
            details = self.data[date]['Details']

            # Подсчитываем количество доходных транзакций
            num_income_transactions = len([detail for detail in details if detail[4] == 'Income'])

            # Суммируем доходы
            total_income = sum([detail[2] for detail in details if detail[4] == 'Income'])

            sel.annotation.set(
                text=f"Количество доходных транзакций: {num_income_transactions}\nОбщая сумма доходов: {total_income:.2f}₽\nДата: {date}")
            sel.annotation.get_bbox_patch().set(fc="#C4E0A6", alpha=0.8)

        # Подсказка для расходов
        @cursor_expense.connect("add")
        def on_add_expense(sel):
            index = sel.index
            date = self.times[index]
            details = self.data[date]['Details']

            # Подсчитываем количество расходных транзакций
            num_expense_transactions = len([detail for detail in details if detail[4] == 'Expense'])

            # Суммируем расходы
            total_expense = sum([detail[2] for detail in details if detail[4] == 'Expense'])

            sel.annotation.set(
                text=f"Количество расходных транзакций: {num_expense_transactions}\nОбщая сумма расходов: {total_expense:.2f}₽\nДата: {date}")
            sel.annotation.get_bbox_patch().set(fc="#FF6F61", alpha=0.9)

        @cursor_income.connect("remove")
        def on_remove_income(sel):
            sel.annotation.set_visible(False)

        @cursor_expense.connect("remove")
        def on_remove_expense(sel):
            sel.annotation.set_visible(False)
