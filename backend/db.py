import sqlite3
import os
from datetime import datetime, timedelta
DATABASE_NAME = "database/accounting.db"


def get_connection():

    connection = sqlite3.connect(DATABASE_NAME)

    return connection


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # =========================
    # Users Table
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        user_id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        email TEXT NOT NULL UNIQUE,

        password TEXT NOT NULL,

        role TEXT NOT NULL DEFAULT 'user'

    )
    """)

    # =========================
    # Expenses Table
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (

        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        expense_name TEXT NOT NULL,

        category TEXT NOT NULL,

        amount REAL NOT NULL,

        expense_date TEXT NOT NULL,

        notes TEXT,

        FOREIGN KEY(user_id)
            REFERENCES users(user_id)

    )
    """)

    # =========================
    # Income Table
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (

        income_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        income_source TEXT NOT NULL,

        amount REAL NOT NULL,

        income_date TEXT NOT NULL,

        notes TEXT,

        FOREIGN KEY(user_id)
            REFERENCES users(user_id)

    )
    """)

    # =========================
    # Documents Table
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        document_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        document_type TEXT NOT NULL,

        file_name TEXT NOT NULL,

        file_path TEXT NOT NULL,

        upload_date TEXT NOT NULL,

        ocr_text TEXT,

        cleaned_text TEXT,

        ai_result TEXT,

        FOREIGN KEY(user_id)
            REFERENCES users(user_id)

    )
    """)

    # =========================
    # Bills Table
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (

        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        document_id INTEGER NOT NULL,

        name TEXT,

        issue_date TEXT,

        bill_month TEXT,

        due_date TEXT,

        reference_no TEXT,

        payable_within_due_date REAL,

        payable_after_due_date REAL,

        created_at TEXT,

        FOREIGN KEY(user_id)
            REFERENCES users(user_id),

        FOREIGN KEY(document_id)
            REFERENCES documents(document_id)

    )
    """)

    # =========================
    # Receipts Table
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts (

        receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        document_id INTEGER NOT NULL,

        amount REAL,

        receiver TEXT,

        sender TEXT,

        transaction_id TEXT,

        transaction_date TEXT,

        created_at TEXT,

        FOREIGN KEY(user_id)
            REFERENCES users(user_id),

        FOREIGN KEY(document_id)
            REFERENCES documents(document_id)

    )
    """)

    connection.commit()

    connection.close()

    print("✅ Database tables created successfully.")





def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


def create_user(
    username,
    email,
    password,
    role="user"
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            email,
            password,
            role
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            email,
            password,
            role
        )
    )

    connection.commit()
    connection.close()



def get_user_role(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None  




def delete_expense(expense_id, user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM expenses

        WHERE expense_id = ?
        AND user_id = ?
        """,
        (expense_id, user_id)
    )

    connection.commit()

    rows_deleted = cursor.rowcount

    connection.close()

    return rows_deleted

def add_income(
    user_id,
    income_source,
    amount,
    income_date,
    notes
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO income
        (
            user_id,
            income_source,
            amount,
            income_date,
            notes
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            income_source,
            amount,
            income_date,
            notes
        )
    )

    connection.commit()

    connection.close()

def get_all_income():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            income.income_id,
            users.username,
            income.income_source,
            income.amount,
            income.income_date

        FROM income

        INNER JOIN users
        ON income.user_id = users.user_id

        ORDER BY income.income_id DESC
        """
    )

    incomes = cursor.fetchall()

    connection.close()

    return incomes

def get_user_income(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            income_id,
            income_source,
            amount,
            income_date,
            notes

        FROM income

        WHERE user_id = ?

        ORDER BY income_id DESC
        """,
        (user_id,)
    )

    incomes = cursor.fetchall()

    connection.close()

    return incomes    


def update_income(
    income_id,
    user_id,
    income_source,
    amount,
    income_date,
    notes
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE income

        SET
            income_source = ?,
            amount = ?,
            income_date = ?,
            notes = ?

        WHERE
            income_id = ?
            AND user_id = ?
        """,
        (
            income_source,
            amount,
            income_date,
            notes,
            income_id,
            user_id
        )
    )

    connection.commit()

    rows_updated = cursor.rowcount

    connection.close()

    return rows_updated

def get_total_income(user_id, date_filter="all"):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT SUM(amount)
        FROM income
        WHERE user_id = ?
    """

    params = [user_id]

    if date_filter == "this_month":

        query += """
            AND strftime('%Y-%m', income_date) = strftime('%Y-%m', 'now')
        """

    elif date_filter == "last_month":

        query += """
            AND strftime('%Y-%m', income_date) =
                strftime('%Y-%m', date('now', '-1 month'))
        """

    elif date_filter == "this_year":

        query += """
            AND strftime('%Y', income_date) = strftime('%Y', 'now')
        """

    cursor.execute(query, params)

    result = cursor.fetchone()

    connection.close()

    if result[0] is None:
        return 0

    return result[0]


def delete_income(income_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM income
        WHERE income_id = ?
        """,
        (income_id,)
    )

    connection.commit()

    rows_deleted = cursor.rowcount

    connection.close()

    return rows_deleted    



def get_days_with_expenses(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT expense_date)
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    if result[0] is None or result[0] == 0:
        return 1

    return result[0]


def predict_monthly_expenses(user_id):

    total_expenses = get_total_expenses(user_id)

    days = get_days_with_expenses(user_id)

    daily_average = total_expenses / days

    predicted_monthly = daily_average * 30

    return round(predicted_monthly, 2)








def admin_delete_expense(expense_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE expense_id = ?
        """,
        (expense_id,)
    )

    connection.commit()

    rows_deleted = cursor.rowcount

    connection.close()

    return rows_deleted    
    



def get_expense_categories(user_id, date_filter="all"):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            category,
            SUM(amount) AS total

        FROM expenses

        WHERE user_id = ?
    """

    params = [user_id]

    if date_filter == "this_month":

        query += """
            AND strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
        """

    elif date_filter == "last_month":

        query += """
            AND strftime('%Y-%m', expense_date) =
                strftime('%Y-%m', date('now', '-1 month'))
        """

    elif date_filter == "this_year":

        query += """
            AND strftime('%Y', expense_date) = strftime('%Y', 'now')
        """

    query += """
        GROUP BY category
        ORDER BY total DESC
    """

    cursor.execute(query, params)

    categories = cursor.fetchall()

    connection.close()

    return categories



def get_monthly_summary(user_id, date_filter="all"):

    connection = get_connection()
    cursor = connection.cursor()

    expense_query = """
        SELECT
            strftime('%Y-%m', expense_date) AS month,
            SUM(amount) AS total_expenses

        FROM expenses

        WHERE user_id = ?
    """

    income_query = """
        SELECT
            strftime('%Y-%m', income_date) AS month,
            SUM(amount) AS total_income

        FROM income

        WHERE user_id = ?
    """

    expense_params = [user_id]
    income_params = [user_id]

    if date_filter == "this_month":

        expense_query += """
            AND strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
        """

        income_query += """
            AND strftime('%Y-%m', income_date) = strftime('%Y-%m', 'now')
        """

    elif date_filter == "last_month":

        expense_query += """
            AND strftime('%Y-%m', expense_date) =
                strftime('%Y-%m', date('now', '-1 month'))
        """

        income_query += """
            AND strftime('%Y-%m', income_date) =
                strftime('%Y-%m', date('now', '-1 month'))
        """

    elif date_filter == "this_year":

        expense_query += """
            AND strftime('%Y', expense_date) = strftime('%Y', 'now')
        """

        income_query += """
            AND strftime('%Y', income_date) = strftime('%Y', 'now')
        """

    expense_query += """
        GROUP BY month
        ORDER BY month
    """

    income_query += """
        GROUP BY month
        ORDER BY month
    """

    cursor.execute(expense_query, expense_params)
    expense_data = cursor.fetchall()

    cursor.execute(income_query, income_params)
    income_data = cursor.fetchall()

    connection.close()

    summary = {}

    # Add income data
    for month, total in income_data:

        summary[month] = {
            "month": month,
            "income": total,
            "expenses": 0
        }

    # Add expense data
    for month, total in expense_data:

        if month in summary:

            summary[month]["expenses"] = total

        else:

            summary[month] = {
                "month": month,
                "income": 0,
                "expenses": total
            }

    return sorted(
        summary.values(),
        key=lambda x: x["month"]
    )





def update_expense(
    expense_id,
    user_id,
    expense_name,
    category,
    amount,
    expense_date,
    notes
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE expenses

        SET
            expense_name = ?,
            category = ?,
            amount = ?,
            expense_date = ?,
            notes = ?

        WHERE
            expense_id = ?
            AND user_id = ?
        """,
        (
            expense_name,
            category,
            amount,
            expense_date,
            notes,
            expense_id,
            user_id
        )
    )

    connection.commit()

    rows_updated = cursor.rowcount

    connection.close()

    return rows_updated



def make_admin(email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET role = 'admin'
        WHERE email = ?
        """,
        (email,)
    )

    connection.commit()

    if cursor.rowcount > 0:
        print("✅ User is now an Admin.")
    else:
        print("❌ User not found.")

    connection.close()



def get_all_users():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 
            user_id,
            username,
            email,
            role
        FROM users
        """
    )

    users = cursor.fetchall()

    connection.close()

    return users



def get_all_expenses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            expenses.expense_id,
            users.username,
            expenses.expense_name,
            expenses.category,
            expenses.amount,
            expenses.expense_date
        FROM expenses
        JOIN users
            ON expenses.user_id = users.user_id
        ORDER BY expenses.expense_date DESC
        """
    )

    expenses = cursor.fetchall()

    connection.close()

    return expenses






def delete_user(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()

    rows_deleted = cursor.rowcount

    connection.close()

    return rows_deleted


def update_user_role(user_id, role):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET role = ?
        WHERE user_id = ?
        """,
        (
            role,
            user_id
        )
    )

    connection.commit()

    rows_updated = cursor.rowcount

    connection.close()

    return rows_updated


def get_total_users():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        """
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_total_admins():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE role = 'admin'
        """
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_system_total_income():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM income
        """
    )

    result = cursor.fetchone()[0]

    connection.close()

    return result if result else 0


def get_system_total_expenses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM expenses
        """
    )

    result = cursor.fetchone()[0]

    connection.close()

    return result if result else 0    


def get_total_expenses(user_id, date_filter="all"):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id = ?
    """

    params = [user_id]

    if date_filter == "this_month":

        query += """
            AND strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
        """

    elif date_filter == "last_month":

        query += """
            AND strftime('%Y-%m', expense_date) =
                strftime('%Y-%m', date('now', '-1 month'))
        """

    elif date_filter == "this_year":

        query += """
            AND strftime('%Y', expense_date) = strftime('%Y', 'now')
        """

    cursor.execute(query, params)

    result = cursor.fetchone()

    connection.close()

    if result[0] is None:
        return 0

    return result[0]






def get_expense_by_category(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            category,
            SUM(amount) as total

        FROM expenses

        WHERE user_id = ?

        GROUP BY category

        ORDER BY total DESC
        """,
        (user_id,)
    )


    expenses = cursor.fetchall()

    connection.close()

    return expenses    


def get_expense_category_summary(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            category,
            SUM(amount)

        FROM expenses

        WHERE user_id = ?

        GROUP BY category

        ORDER BY SUM(amount) DESC
        """,
        (user_id,)
    )

    result = cursor.fetchall()

    connection.close()

    return result    





def get_documents_by_user(user_id):

    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM documents
        WHERE user_id = ?
        ORDER BY document_id DESC
    """, (user_id,))

    documents = cursor.fetchall()

    connection.close()

    return [dict(doc) for doc in documents]




# =========================
# Create Document
# =========================

def create_document(
    user_id,
    document_type,
    file_name,
    file_path,
    ocr_text,
    cleaned_text,
    ai_result
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents
        (
            user_id,
            document_type,
            file_name,
            file_path,
            upload_date,
            ocr_text,
            cleaned_text,
            ai_result
        )

        VALUES
        (
            ?, ?, ?, ?, date('now'),
            ?, ?, ?
        )
        """,
        (
            user_id,
            document_type,
            file_name,
            file_path,
            ocr_text,
            cleaned_text,
            ai_result
        )
    )

    document_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return document_id


# =========================
# Create Bill
# =========================

def create_bill(
    user_id,
    document_id,
    name,
    issue_date,
    bill_month,
    due_date,
    reference_no,
    payable_within_due_date,
    payable_after_due_date
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bills
        (
            user_id,
            document_id,
            name,
            issue_date,
            bill_month,
            due_date,
            reference_no,
            payable_within_due_date,
            payable_after_due_date,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            user_id,
            document_id,
            name,
            issue_date,
            bill_month,
            due_date,
            reference_no,
            payable_within_due_date,
            payable_after_due_date
        )
    )

    bill_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return bill_id



# =========================
# Create Receipt
# =========================

def create_receipt(
    user_id,
    document_id,
    amount,
    receiver,
    sender,
    transaction_id,
    transaction_date
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO receipts
        (
            user_id,
            document_id,
            amount,
            receiver,
            sender,
            transaction_id,
            transaction_date,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            user_id,
            document_id,
            amount,
            receiver,
            sender,
            transaction_id,
            transaction_date
        )
    )

    receipt_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return receipt_id


def get_receipts_by_user(user_id):

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM receipts
        WHERE user_id = ?
        ORDER BY receipt_id DESC
        """,
        (user_id,)
    )

    receipts = cursor.fetchall()

    connection.close()

    return [dict(receipt) for receipt in receipts]


def get_bills_by_user(user_id):

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM bills
        WHERE user_id = ?
        ORDER BY bill_id DESC
        """,
        (user_id,)
    )

    bills = cursor.fetchall()

    connection.close()

    return [dict(bill) for bill in bills]


def get_all_receipts():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            receipts.receipt_id,
            users.username,
            receipts.amount,
            receipts.receiver,
            receipts.sender,
            receipts.transaction_id,
            receipts.transaction_date
        FROM receipts

        JOIN users
        ON receipts.user_id = users.user_id

        ORDER BY receipts.receipt_id DESC
        """
    )

    receipts = cursor.fetchall()

    connection.close()

    return receipts


def get_all_bills():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            bills.bill_id,
            users.username,
            bills.name,
            bills.issue_date,
            bills.bill_month,
            bills.due_date,
            bills.reference_no,
            bills.payable_within_due_date,
            bills.payable_after_due_date
        FROM bills

        JOIN users
        ON bills.user_id = users.user_id

        ORDER BY bills.bill_id DESC
        """
    )

    bills = cursor.fetchall()

    connection.close()

    return bills


if __name__ == "__main__":

    create_tables()  
     