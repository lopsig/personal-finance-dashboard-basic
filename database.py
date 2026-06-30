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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            monthly_budget REAL NOT NULL
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO settings (
            id,
            monthly_budget
        )
        VALUES (1, 300.00)
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



def get_budget():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT monthly_budget
        FROM settings
        WHERE id = 1
    """)

    result = cursor.fetchone()

    conn.close()

    return result[0]

def update_budget(new_budget):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE settings
        SET monthly_budget = ?
        WHERE id = 1
    """, (new_budget,))

    conn.commit()
    conn.close()


#UPDATE EXPENSES
def update_expense(expense_id, date, category, amount, description):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET
            date = ?,
            category = ?,
            amount = ?,
            description = ?
        WHERE id = ?
    """, (
        date,
        category,
        amount,
        description,
        expense_id
    ))

    conn.commit()
    conn.close()

#DELETE EXPENSES

def delete_expense(expense_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    conn.commit()
    conn.close()