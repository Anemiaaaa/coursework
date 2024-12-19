import sqlite3
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Frame, messagebox, Listbox, Label, END, Toplevel, CENTER
from pathlib import Path
import subprocess
from openpyxl import Workbook
from tkinter import filedialog
from tkcalendar import DateEntry
from openpyxl import Workbook
from datetime import datetime


class Settings(Frame):
    def __init__(self, parent_frame, assets_path, username):
        super().__init__(parent_frame)  # Привязываем к родительскому фрейму
        self.parent_frame = parent_frame
        self.assets_path = assets_path
        self.username = username
        self.setup_ui()
        self.dbpath = r'C:\Users\amiri\PycharmProjects\kursach\экраны\cointracker.db'

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_ui(self):
        self.canvas = Canvas(
            self.parent_frame,
            bg="#C4E0A6",
            height=637,
            width=762,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0.0, 125.0, 762.0, 445.0, fill="#74C38C", outline="")

        # Поля для ввода нового пароля
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(229.5, 371.5, image=self.entry_image_1)
        self.entry_1 = Entry(self.parent_frame, bd=0, bg="#8FEAAB", fg="#000716", highlightthickness=0, show='*',
                             font=("Arial", 16))
        self.entry_1.place(x=154.0, y=350.0, width=151.0, height=43.0)

        # Поля для ввода старого пароля
        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(229.5, 256.5, image=self.entry_image_3)
        self.entry_3 = Entry(self.parent_frame, bd=0, bg="#8FEAAB", fg="#000716", highlightthickness=0, show='*',
                             font=("Arial", 16))
        self.entry_3.place(x=154.0, y=235.0, width=151.0, height=43.0)

        # Кнопка для изменения пароля
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.parent_frame,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.change_password,
            relief="flat"
        )
        self.button_3.place(x=427.0, y=267.0, width=190.0, height=58.0)

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_4 = Button(
            self.parent_frame,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.export_to_excel,
            relief="flat"
        )
        self.button_4.place(
            x=522.0,
            y=504.0,
            width=228.0,
            height=60.24080276489258
        )

        # Кнопка для удаления пользователя
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.parent_frame,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_user,
            relief="flat"
        )
        self.button_1.place(
            x=273.0,
            y=504.0,
            width=228.0,
            height=60.24080276489258
        )

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_2 = Button(
            self.parent_frame,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_authorization_window,
            relief="flat"
        )
        self.button_2.place(
            x=522.0,
            y=38.0,
            width=187.0,
            height=62.33333206176758
        )

        # Кнопка для удаления всех транзакций
        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_5 = Button(
            self.parent_frame,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_all_transactions,
            relief="flat"
        )
        self.button_5.place(
            x=24.0,
            y=504.0,
            width=228.0,
            height=60.24080276489258
        )





        # Прочие элементы интерфейса
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(225.0, 328.0, image=self.image_image_1)

        self.canvas.create_rectangle(-2.0, 123.0, 761.9999901050287, 125.99999999027409, fill="#000000", outline="")
        self.canvas.create_rectangle(-2.0, 443.0, 761.9999901050287, 445.9999999902741, fill="#000000", outline="")

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(222.0, 213.0, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(181.0, 67.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(384.0, 163.0, image=self.image_image_4)



        self.parent_frame.update()  # Обновляем родительский фрейм для отображения всех элементов

    def export_to_excel(self):
        """Открывает окно для выбора диапазона дат и экспортирует данные из базы данных в Excel."""
        def open_date_range_window():
            """Открывает окно для выбора начальной и конечной дат."""
            date_window = Toplevel()
            date_window.title("Выбор диапазона дат")
            date_window.geometry("300x250")
            date_window.resizable(False, False)
            date_window.configure(bg="#C4E0A6")

            # Центрируем окно на экране
            date_window.update_idletasks()
            x = (date_window.winfo_screenwidth() // 2) - (300 // 2)
            y = (date_window.winfo_screenheight() // 2) - (250 // 2)
            date_window.geometry(f"+{x}+{y}")


            Label(date_window, text="Выберите диапазон дат", font=("Arial", 12, "bold"), anchor=CENTER, bg="#C4E0A6").pack(pady=10)

            Label(date_window, text="Начальная дата:", font=("Arial", 10), bg="#C4E0A6").pack(pady=5)
            start_date_entry = DateEntry(date_window, width=12, background='darkblue', foreground='white', borderwidth=2)
            start_date_entry.pack(pady=5)

            Label(date_window, text="Конечная дата:", font=("Arial", 10), bg="#C4E0A6").pack(pady=5)
            end_date_entry = DateEntry(date_window, width=12, background='darkblue', foreground='white', borderwidth=2)
            end_date_entry.pack(pady=5)

            def confirm_dates():
                # Получаем даты из виджетов
                start_date = datetime.strptime(start_date_entry.get(), "%m/%d/%y").strftime("%Y-%m-%d")
                end_date = datetime.strptime(end_date_entry.get(), "%m/%d/%y").strftime("%Y-%m-%d")
                date_window.destroy()
                perform_export(start_date, end_date)

            confirm_button = Button(date_window, text="Экспортировать", command=confirm_dates, bg="green", fg="white", font=("Arial", 10, "bold"))
            confirm_button.place(relx=0.5, rely=0.9, anchor=CENTER)

            def confirm_dates():
                # Получаем даты из виджетов
                start_date = datetime.strptime(start_date_entry.get(), "%m/%d/%y").strftime("%Y-%m-%d")
                end_date = datetime.strptime(end_date_entry.get(), "%m/%d/%y").strftime("%Y-%m-%d")
                date_window.destroy()
                perform_export(start_date, end_date)

            confirm_button = Button(date_window, text="Экспортировать", command=confirm_dates, bg="green", fg="white", font=("Arial", 10, "bold"))
            confirm_button.place(relx=0.5, rely=0.9, anchor=CENTER)

        def perform_export(start_date, end_date):
            try:
                # Открываем диалоговое окно для выбора пути сохранения файла
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
                    title="Сохранить файл как"
                )

                if not file_path:  # Если пользователь закрыл окно, не выбирая файл
                    return

                conn = sqlite3.connect(self.dbpath)
                cursor = conn.cursor()

                # Преобразуем даты в нужный формат для SQL-запроса
                cursor.execute('''
                    SELECT t.TransactionID, t.UserID, t.Amount, t.Type, t.Date, t.Description,
                           ic.name AS IncomeCategory, ec.name AS ExpenseCategory
                    FROM Transactions t
                    LEFT JOIN IncomeCategories ic ON t.IncomeCategoryID = ic.id
                    LEFT JOIN ExpenseCategories ec ON t.ExpenseCategoryID = ec.id
                    WHERE t.UserID = (SELECT id FROM Users WHERE username = ?)
                      AND SUBSTR(t.Date, 1, 10) >= ?
                      AND SUBSTR(t.Date, 1, 10) <= ?
                ''', (self.username, start_date, end_date))
                transactions = cursor.fetchall()

                # Диагностика: вывод количества транзакций в консоль
                print(f"Найдено {len(transactions)} транзакций в диапазоне {start_date} - {end_date}")

                if not transactions:
                    messagebox.showinfo("Информация", "За выбранный период транзакций не найдено.")
                    conn.close()
                    return

                # Создаем новый Excel-файл
                wb = Workbook()
                ws = wb.active
                ws.title = "Транзакции"

                # Добавляем заголовки
                headers = ["TransactionID", "UserID", "Amount", "Type", "Date", "Description", "IncomeCategory",
                           "ExpenseCategory"]
                ws.append(headers)

                # Добавляем данные
                for transaction in transactions:
                    ws.append(transaction)

                # Сохраняем файл
                wb.save(file_path)
                conn.close()

                messagebox.showinfo("Успех", f"Данные успешно экспортированы в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {e}")

        open_date_range_window()


    def change_password(self):
        """Изменяет пароль пользователя."""
        old_password = self.entry_3.get()
        new_password = self.entry_1.get()


        if not old_password or not new_password:
            messagebox.showerror("Ошибка", "Пожалуйста, введите старый и новый пароли.")
            return

        if self.check_old_password(old_password):
            # Обновляем пароль в базе данных
            self.update_password_in_db(new_password)
            messagebox.showinfo("Успех", "Пароль успешно изменен!")
        else:
            messagebox.showerror("Ошибка", "Неверный старый пароль!")

    def check_old_password(self, old_password):
        """Проверяет старый пароль пользователя в базе данных."""
        conn = sqlite3.connect(self.dbpath)  # Подключаемся к базе данных
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM Users WHERE username = ?', (self.username,))  # Запрос для получения пароля
        result = cursor.fetchone()  # Получаем результат

        conn.close()

        if result and result[0] == old_password:
            return True
        return False

    def update_password_in_db(self, new_password):
        """Обновляет новый пароль пользователя в базе данных."""
        conn = sqlite3.connect(self.dbpath)  # Подключаемся к базе данных
        cursor = conn.cursor()

        cursor.execute('UPDATE Users SET password = ? WHERE username = ?',
                       (new_password, self.username))  # Запрос на обновление пароля
        conn.commit()  # Сохраняем изменения
        conn.close()

    def delete_all_transactions(self):
        """Удаляет все транзакции пользователя из базы данных."""
        conn = sqlite3.connect(self.dbpath)  # Подключаемся к базе данных
        cursor = conn.cursor()

        # Получаем user_id текущего пользователя
        cursor.execute('SELECT id FROM Users WHERE username = ?', (self.username,))
        user_id = cursor.fetchone()

        if user_id:
            cursor.execute('DELETE FROM Transactions WHERE UserID = ?',
                           (user_id[0],))  # Удаляем все транзакции пользователя
            conn.commit()  # Сохраняем изменения
            messagebox.showinfo("Успех", "Все транзакции были удалены!")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден!")

        conn.close()

    def delete_user(self):
        """Удаляет пользователя из базы данных после подтверждения."""
        response = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить свой аккаунт?")

        if response:  # Если пользователь подтвердил
            conn = sqlite3.connect(self.dbpath)  # Подключаемся к базе данных
            cursor = conn.cursor()

            # Получаем user_id текущего пользователя
            cursor.execute('SELECT id FROM Users WHERE username = ?', (self.username,))
            user_id = cursor.fetchone()

            if user_id:
                # Удаляем все данные пользователя (его аккаунт и транзакции)
                cursor.execute('DELETE FROM Transactions WHERE UserID = ?', (user_id[0],))
                cursor.execute('DELETE FROM Users WHERE id = ?', (user_id[0],))
                conn.commit()  # Сохраняем изменения

                messagebox.showinfo("Успех", "Ваш аккаунт был удален.")
                conn.close()
                self.open_authorization_window()  # Открываем окно авторизации
            else:
                conn.close()
                messagebox.showerror("Ошибка", "Пользователь не найден!")

    def open_authorization_window(self):
        """Закрывает текущее окно и открывает окно авторизации."""
        self.parent_frame.master.destroy()  # Удаляем основное окно
        # Запускаем окно авторизации (например, subprocess для авторизационного окна)
        subprocess.Popen(["python", "autorizacia.py"])  # Замените на путь к вашему файлу авторизации
