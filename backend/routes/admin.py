from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from openai import OpenAI

from db import (
    get_all_users,
    delete_user,
    get_all_income,
    delete_income,
    get_all_expenses,
    delete_expense,
    update_user_role,
    get_total_users,
    get_total_admins,
    get_system_total_income,
    get_system_total_expenses,
    get_all_receipts,
    get_all_bills
)


admin_bp = Blueprint(
    "admin",
    __name__
)


# ==============================
# Get All Users
# ==============================

@admin_bp.route("/admin/users", methods=["GET"])
@jwt_required()
def admin_users():

    users = get_all_users()

    user_list = []

    for user in users:

        user_list.append(
            {
                "user_id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3]
            }
        )

    return jsonify(
        {
            "users": user_list
        }
    ), 200


# ==============================
# Delete User
# ==============================

@admin_bp.route("/admin/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def remove_user(user_id):

    rows_deleted = delete_user(user_id)

    if rows_deleted == 0:

        return jsonify(
            {
                "message": "User not found."
            }
        ), 404

    return jsonify(
        {
            "message": "User deleted successfully."
        }
    ), 200


# ==============================
# Update User Role
# ==============================

@admin_bp.route("/admin/users/<int:user_id>/role", methods=["PUT"])
@jwt_required()
def change_user_role(user_id):

    data = request.get_json()

    role = data.get("role")

    if role not in ["admin", "user"]:

        return jsonify(
            {
                "message": "Invalid role."
            }
        ), 400

    rows_updated = update_user_role(
        user_id,
        role
    )

    if rows_updated == 0:

        return jsonify(
            {
                "message": "User not found."
            }
        ), 404

    return jsonify(
        {
            "message": "User role updated successfully."
        }
    ), 200


# ==============================
# Get All Expenses
# ==============================

@admin_bp.route("/admin/expenses", methods=["GET"])
@jwt_required()
def admin_expenses():

    expenses = get_all_expenses()

    expense_list = []

    for expense in expenses:

        expense_list.append(
            {
                "expense_id": expense[0],
                "username": expense[1],
                "expense_name": expense[2],
                "category": expense[3],
                "amount": expense[4],
                "expense_date": expense[5]
            }
        )

    return jsonify(
        {
            "expenses": expense_list
        }
    ), 200


# ==============================
# Delete Expense
# ==============================

@admin_bp.route("/admin/expenses/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense_by_admin(expense_id):

    deleted = delete_expense(expense_id)

    if deleted == 0:

        return jsonify(
            {
                "message": "Expense not found."
            }
        ), 404

    return jsonify(
        {
            "message": "Expense deleted successfully."
        }
    ), 200


# ==============================
# Get All Income
# ==============================

@admin_bp.route("/admin/income", methods=["GET"])
@jwt_required()
def admin_income():

    incomes = get_all_income()

    income_list = []

    for income in incomes:

        income_list.append(
            {
                "income_id": income[0],
                "username": income[1],
                "source": income[2],
                "amount": income[3],
                "income_date": income[4]
            }
        )

    return jsonify(
        {
            "income": income_list
        }
    ), 200


# ==============================
# Delete Income
# ==============================

@admin_bp.route("/admin/income/<int:income_id>", methods=["DELETE"])
@jwt_required()
def admin_delete_income(income_id):

    deleted = delete_income(income_id)

    if deleted == 0:

        return jsonify(
            {
                "message": "Income not found."
            }
        ), 404

    return jsonify(
        {
            "message": "Income deleted successfully."
        }
    ), 200


# =========================================================
# Get All Receipts
# =========================================================

@admin_bp.route("/admin/receipts", methods=["GET"])
@jwt_required()
def admin_receipts():

    receipts = get_all_receipts()

    receipt_list = []

    for receipt in receipts:

        receipt_list.append(
            {
                "receipt_id": receipt[0],
                "username": receipt[1],
                "amount": receipt[2],
                "receiver": receipt[3],
                "sender": receipt[4],
                "transaction_id": receipt[5],
                "transaction_date": receipt[6]
            }
        )

    return jsonify(
        {
            "receipts": receipt_list
        }
    ), 200


# =========================================================
# Get All Bills
# =========================================================

@admin_bp.route("/admin/bills", methods=["GET"])
@jwt_required()
def admin_bills():

    bills = get_all_bills()

    bill_list = []

    for bill in bills:

        bill_list.append(
            {
                "bill_id": bill[0],
                "username": bill[1],
                "name": bill[2],
                "issue_date": bill[3],
                "bill_month": bill[4],
                "due_date": bill[5],
                "reference_no": bill[6],
                "payable_within_due_date": bill[7],
                "payable_after_due_date": bill[8]
            }
        )

    return jsonify(
        {
            "bills": bill_list
        }
    ), 200


# ==============================
# Dashboard Statistics
# ==============================

@admin_bp.route("/admin/stats", methods=["GET"])
@jwt_required()
def admin_stats():

    return jsonify(
        {
            "total_users": get_total_users(),
            "total_admins": get_total_admins(),
            "total_income": get_system_total_income(),
            "total_expenses": get_system_total_expenses()
        }
    ), 200


# ==============================
# AI Summary
# ==============================

@admin_bp.route("/admin/ai-summary", methods=["GET"])
@jwt_required()
def admin_ai_summary():

    total_users = get_total_users()
    total_admins = get_total_admins()
    total_income = get_system_total_income()
    total_expenses = get_system_total_expenses()

    client = OpenAI()

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",
                "content": "You are a professional financial analyst."
            },

            {
                "role": "user",
                "content": f"""
Total Users: {total_users}

Total Admins: {total_admins}

Total Income: Rs. {total_income}

Total Expenses: Rs. {total_expenses}

Generate a short financial summary for the administrator.
"""
            }

        ]

    )

    ai_summary = response.choices[0].message.content

    return jsonify(
        {
            "ai_summary": ai_summary
        }
    ), 200


