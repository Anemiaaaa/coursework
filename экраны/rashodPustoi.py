import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path
from tkinter import Frame, Canvas, PhotoImage, StringVar, Label, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from calendar import month_name


class RashodPustoi(Frame):
    def __init__(self, parent, assets_path, username):
        super().__init__(parent)
        self.frame = parent
        self.assets_path = assets_path
        self.logged_in_user = username
        self.current_date = datetime.now()  # Текущая дата
        self.month_offset = 0  # Смещение по месяцам (для переключения)
        self.period = StringVar(value="month")  # Переменная для выбора периода
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_ui(self):
        """Настройка интерфейса и отображение графика"""
        self.canvas = Canvas(
            self.frame,
            bg="#74C38C",  # Устанавливаем цвет фона канваса
            height=800,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Создание надписи с текущим месяцем
        self.month_label = Label(self.frame, text=self.get_month_name(), bg="#74C38C",
                                 font=("Century Gothic", 18, 'bold'), fg="black")
        self.month_label.place(x=450, y=10)

        # Генерация данных и создание графика
        self.data = self.generate_data_from_db()
        self.create_graph()

        # Кнопки для переключения месяцев
        prev_button = Button(self.frame, text="<", command=self.show_previous_month, font=("Century Gothic", 14),
                             bg="#74C38C", fg="black")
        prev_button.place(x=500, y=300)

        next_button = Button(self.frame, text=">", command=self.show_next_month, font=("Century Gothic", 14),
                             bg="#74C38C", fg="black")
        next_button.place(x=530, y=300)

        # Если для текущего месяца есть данные, отображаем текст
        if self.data[0]:  # Если есть данные для категорий
            self.create_text_lines()

    def generate_data_from_db(self):
        """Получение данных из базы данных для графика (доходы)"""
        conn = sqlite3.connect('C:\\Users\\amiri\\PycharmProjects\\kursach\\экраны\\cointracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM Users WHERE username = ?', (self.logged_in_user,))
        user_id = cursor.fetchone()

        # Получаем данные по транзакциям для текущего пользователя
        target_month = self.current_date.month - self.month_offset
        target_year = self.current_date.year

        # Корректируем месяц и год для правильной фильтрации
        if target_month < 1:
            target_month += 12
            target_year -= 1
        elif target_month > 12:
            target_month -= 12
            target_year += 1

        start_date = datetime(target_year, target_month, 1)
        if target_month == 12:
            end_date = datetime(target_year + 1, 1, 1)
        else:
            end_date = datetime(target_year, target_month + 1, 1)

        query = '''
        SELECT Date, Type, Amount, Description, IncomeCategoryID
        FROM Transactions
        WHERE UserID = ? AND Type = "Income" AND Date BETWEEN ? AND ?
        '''
        cursor.execute(query, (user_id[0], start_date, end_date))
        transactions = cursor.fetchall()

        # Получаем названия категорий доходов
        income_categories = {}
        cursor.execute('SELECT id, name FROM IncomeCategories')
        for row in cursor.fetchall():
            income_categories[row[0]] = row[1]

        # Подсчитываем суммы доходов по категориям
        income_sums = {}
        income_counts = {}
        for transaction in transactions:
            category_id = transaction[4]
            amount = transaction[2]
            if category_id not in income_sums:
                income_sums[category_id] = 0
                income_counts[category_id] = 0
            income_sums[category_id] += amount
            income_counts[category_id] += 1

        # Если данных нет, возвращаем пустые значения
        if not income_sums:
            return [], [], income_categories

        # Создаем список для графика
        labels = [income_categories[cat_id] for cat_id in income_sums]
        values = list(income_sums.values())
        counts = list(income_counts.values())

        return labels, values, counts, income_categories

    def create_graph(self):
        """Создание графика (круговая диаграмма для доходов)"""
        labels, values, _, _ = self.data

        # Проверка, есть ли данные для графика
        if not labels or not values:
            # Если данных нет, отображаем пустой график с заголовком
            fig, ax = plt.subplots(figsize=(4.5, 3.5))
            ax.set_title("Нет данных для отображения", fontsize=12)
            ax.axis('off')  # Выключаем оси
            fig.patch.set_facecolor("#74C38C")
        else:
            # Построение круговой диаграммы
            fig, ax = plt.subplots(figsize=(4.5, 3.5))
            wedges, texts = ax.pie(
                values,
                labels=labels,
                startangle=90,
                colors=plt.cm.Paired.colors,
                wedgeprops=dict(width=0.3, edgecolor='black', linewidth=1)
            )

            # Изменение шрифта подписей на "Century Gothic"
            for text in texts:
                text.set_fontsize(8)  # Уменьшено до 8
                text.set_fontname('Century Gothic')  # Устанавливаем шрифт

            # Равное соотношение сторон
            ax.axis('equal')

            # Установка фона
            fig.patch.set_facecolor("#74C38C")

        # Вставка графика в tkinter окно
        self.canvas_graph = FigureCanvasTkAgg(fig, self.frame)
        self.canvas_graph.get_tk_widget().place(x=0, y=0)

    def create_text_lines(self):
        """Создание строк с категориями, суммами и количеством транзакций"""
        labels, values, counts, _ = self.data

        # Создание меток для каждой строки
        y_offset = 60  # Начальная позиция по оси Y для текста

        for label, value, count in zip(labels, values, counts):
            # Формирование текста для отображения
            text = f"{label}: {value}, Операций: {count}"

            # Создание метки для каждой строки
            label_text = Label(self.frame, text=text, bg="#74C38C", font=("Century Gothic", 11, 'bold'), anchor="w",
                               fg="Black")
            label_text.place(x=430, y=y_offset, width=800, height=30)  # Размещение метки с отступом по Y

            y_offset += 35  # Увеличиваем отступ по Y для следующей строки


    def get_month_name(self):
        """Получение названия месяца для текущего отображаемого месяца"""
        month_num = (self.current_date.month - 1 + self.month_offset) % 12 + 1
        return f"{month_name[month_num]} {self.current_date.year}"

    def show_previous_month(self):
        """Переключение на предыдущий месяц"""
        self.month_offset -= 1
        # Корректируем год, если месяц становится декабрем
        if (self.current_date.month - 1 + self.month_offset) % 12 + 1 == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1)
        self.update_graph()

    def show_next_month(self):
        """Переключение на следующий месяц"""
        self.month_offset += 1
        # Корректируем год, если месяц становится январем
        if (self.current_date.month - 1 + self.month_offset) % 12 + 1 == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1)
        self.update_graph()

    def update_graph(self):
        """Обновление графика и текста при смене месяца"""
        self.data = self.generate_data_from_db()

        # Удаляем старый график и текст
        if hasattr(self, 'canvas_graph'):
            self.canvas_graph.get_tk_widget().destroy()

        for widget in self.frame.winfo_children():
            if isinstance(widget, Label) and widget != self.month_label:  # Убираем только текстовые метки
                widget.destroy()

        # Проверяем, есть ли данные для отображения
        if self.data[0]:  # Если есть данные для доходов
            # Создаем новый график
            self.create_graph()

            # Обновляем надпись с месяцем
            self.month_label.config(text=self.get_month_name())

            # Создаем текстовые метки для категорий доходов
            self.create_text_lines()
        else:
            # Если данных нет, показываем только сообщение "Нет данных"
            fig, ax = plt.subplots(figsize=(4.5, 3.5))
            ax.set_title("Нет данных для отображения", fontsize=12)
            ax.axis('off')  # Выключаем оси
            fig.patch.set_facecolor("#74C38C")

            # Вставляем пустой график в tkinter окно
            self.canvas_graph = FigureCanvasTkAgg(fig, self.frame)
            self.canvas_graph.get_tk_widget().place(x=0, y=0)

            # Обновляем текстовую метку
            self.month_label.config(text=f"{self.get_month_name()} \n (Нет данных)")
