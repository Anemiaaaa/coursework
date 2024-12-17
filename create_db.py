
import sqlite3

try:
    # Подключение к базе данных (или создание, если она не существует)
    conn = sqlite3.connect('C:\\Users\\amiri\\PycharmProjects\\kursach\\экраны\\cointracker.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        balance REAL DEFAULT 0.0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # Создание таблицы категорий доходов
    cursor.execute('''CREATE TABLE IF NOT EXISTS IncomeCategories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )''')

    # Создание таблицы категорий расходов
    cursor.execute('''CREATE TABLE IF NOT EXISTS ExpenseCategories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )''')

    # Создание таблицы для транзакций (доходов и расходов)
    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        IncomeCategoryID INTEGER,
        ExpenseCategoryID INTEGER,
        Amount DECIMAL(15, 2) NOT NULL,
        Type TEXT NOT NULL CHECK (Type IN ('Income', 'Expense')),
        Date DATETIME DEFAULT CURRENT_TIMESTAMP,
        Description TEXT,
        FOREIGN KEY(UserID) REFERENCES Users(UserID),
        FOREIGN KEY(IncomeCategoryID) REFERENCES IncomeCategories(id) ON DELETE SET NULL,
        FOREIGN KEY(ExpenseCategoryID) REFERENCES ExpenseCategories(id) ON DELETE SET NULL
    )''')

    # Вставка данных в таблицу пользователей
    cursor.execute('''INSERT INTO Users (username, password, balance)
    VALUES
    ('amir', '030807', 1000.0),
    ('imam', 'password', 500.0)''')

    # Вставка данных в таблицу категорий доходов
    cursor.execute('''INSERT INTO IncomeCategories (name, description)
    VALUES
    ('Зарплата', 'Доход от основной работы'),
    ('Подарок', 'Получение подарков от друзей или родственников'),
    ('Стипендия', 'Платежи за обучение'),
    ('Подработка', 'Дополнительный доход'),
    ('% от вклада', 'Проценты по банковскому вкладу'),
    ('Карманные', 'Постоянные деньги от родителей')''')

    # Вставка данных в таблицу категорий расходов
    cursor.execute('''INSERT INTO ExpenseCategories (name, description)
    VALUES
    ('Продукты', 'Траты на еду и напитки'),
    ('Транспорт', 'Расходы на проезд'),
    ('Одежда', 'Покупка одежды'),
    ('ЖКХ', 'Коммунальные услуги'),
    ('Связь', 'Оплата мобильной связи и интернета'),
    ('Подарок', 'Подарки друзьям и близким')''')

    # Вставка данных в таблицу транзакций
    cursor.execute('''INSERT INTO Transactions (UserID, IncomeCategoryID, ExpenseCategoryID, Amount, Type, Description)
    VALUES
    (1, 1, NULL, 5000.0, 'Income', 'Зарплата за ноябрь'),
    (1, NULL, 1, 1200.0, 'Expense', 'Купил шоколадку'),
    (1, 2, NULL, 5000.0, 'Income', 'Подарок от бабушки на день рождения'),
    (1, NULL, 3, 300.0, 'Expense', 'Покупка одежды'),
    (1, 3, NULL, 200.0, 'Income', 'Стипендия за ноябрь'),
    (1, NULL, 4, 500.0, 'Expense', 'Коммунальные услуги за ноябрь')''')

    # Сохранение изменений
    conn.commit()

    print("Данные успешно добавлены в базу данных.")

except sqlite3.Error as e:
    print(f"Ошибка при работе с базой данных: {e}")

finally:
    conn.close()