import sys
import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from datetime import datetime

# Get the category passed as command-line argument
if len(sys.argv) > 1:
    category = sys.argv[1]
else:
    category = None

if len(sys.argv) > 1:
    logged_in_user = sys.argv[2]
else:
    logged_in_user = None

if len(sys.argv) > 1:
    Type = sys.argv[3]
else:
    Type = None

print(f"Logged in user: {logged_in_user}, Category: {category}, Type: {Type}")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame SummaOpisanie")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Function to add transaction to the database
def add_transaction(amount, description):
    # Check if the amount is empty
    if not amount:
        messagebox.showerror("Ошибка", "Сумма обязательно должна быть указана!")
        return

    try:
        amount = float(amount)  # Convert amount to float

        # Connect to the database
        conn = sqlite3.connect('cointracker.db')
        cursor = conn.cursor()

        # Insert a new transaction into the database
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('SELECT id FROM Users WHERE username = ?', (logged_in_user,))
        user_id = cursor.fetchone()

        if user_id is None:
            messagebox.showerror("Ошибка", "Пользователь не найден!")
            conn.close()
            return

        # Fetch current balance for the user
        cursor.execute('SELECT balance FROM Users WHERE id = ?', (user_id[0],))
        balance = cursor.fetchone()

        if balance is None:
            messagebox.showerror("Ошибка", "Не удалось получить баланс пользователя.")
            conn.close()
            return

        balance = balance[0]  # Current balance

        # Debug print to check the values being passed
        print(
            f"Inserting transaction: UserID={user_id}, IncomeCategoryID={category}, Amount={amount}, Type={Type}, Description={description}")

        if Type == "Income":
            cursor.execute(""" 
                INSERT INTO Transactions (UserID, IncomeCategoryID, ExpenseCategoryID, Amount, Type, Date, Description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id[0], int(category), None, amount, "Income", date, description))

        if Type == "Expense":
            if amount > balance:  # Check if the expense amount is greater than the current balance
                messagebox.showerror("Ошибка", "Недостаточно средств на счете для выполнения расхода!")
            else:
                cursor.execute(""" 
                    INSERT INTO Transactions (UserID, IncomeCategoryID, ExpenseCategoryID, Amount, Type, Date, Description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id[0], None, int(category), amount, "Expense", date, description))

        conn.commit()

        # Check if the commit was successful
        if conn.total_changes > 0:
            print("Transaction successfully added!")
            messagebox.showinfo("Успех", "Транзакция успешно добавлена!")
        else:
            print("Transaction failed.")

        conn.close()

    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат суммы! Пожалуйста, введите число.")


# GUI setup
window = Tk()
window.geometry("439x414")
window.configure(bg="#C4E0A6")

canvas = Canvas(
    window,
    bg="#C4E0A6",
    height=414,
    width=439,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    -6.499937485792088,
    89.73707292562653,
    549.0001250284158,
    101.26293562568912,
    fill="#63BD03",
    outline="")

# Entry for Amount
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    220.0,
    173.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#8FEAAB",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 16),
)
entry_1.place(
    x=89.0,
    y=155.0,
    width=262.0,
    height=39.0
)

# Entry for Description
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    220.0,
    266.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#8FEAAB",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 16),
)
entry_2.place(
    x=89.0,
    y=248.0,
    width=262.0,
    height=39.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    219.0,
    56.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    121.0,
    134.0,
    image=image_image_2
)

# Button to add transaction
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_transaction(
        entry_1.get(),  # Amount from entry_1
        entry_2.get(),  # Description from entry_2  # Fixed to "Expense" because we are only adding expenses
    ),
    relief="flat"
)
button_1.place(
    x=132.0,
    y=312.0,
    width=175.0,
    height=39.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    220.0,
    227.0,
    image=image_image_3
)

# Now you can use `category` and `logged_in_user` in this window as needed.
window.resizable(False, False)
window.mainloop()
