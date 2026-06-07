import sqlite3

DATABASE_NAME = "finance.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    """)

    connection.commit()
    connection.close()



def insert_expense(date, category, amount, description):

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO expenses (
                   date, 
                   category, 
                   amount, 
                   description
                   ) 
                   VALUES (?, ?, ?, ?)""",
        (date, category, amount, description)
    )
    connection.commit()
    connection.close()



def get_expenses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    conn.close()

    return expenses



def insert_income(date, amount, description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                INSERT INTO incomes (
                date,
                amount,
                description
                )
                VALUES (?, ?, ?)""",
        (date, amount, description))


    connection.commit()
    connection.close()

def get_incomes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM incomes
        ORDER BY id DESC
    """)

    incomes = cursor.fetchall()
    conn.close()

    return incomes

