from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import get_connection, delete_expense, update_expense

expense_bp = Blueprint(
    "expenses",
    __name__
)


# ==========================
# Add Expense
# ==========================
@expense_bp.route("/expenses", methods=["POST"])
@jwt_required()
def add_expense():

    data = request.get_json()

    expense_name = data.get("expense_name")
    category = data.get("category")
    amount = data.get("amount")
    expense_date = data.get("expense_date")
    notes = data.get("notes")

    # Logged-in user id
    user_id = get_jwt_identity()

    if not expense_name or not category or not amount or not expense_date:

        return jsonify({
            "message": "Required fields missing."
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO expenses
        (
            user_id,
            expense_name,
            category,
            amount,
            expense_date,
            notes
        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            expense_name,
            category,
            amount,
            expense_date,
            notes
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Expense added successfully."
    }), 201


# ==========================
# Get Expenses
# ==========================
@expense_bp.route("/expenses", methods=["GET"])
@jwt_required()
def get_expenses():

    user_id = get_jwt_identity()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            expense_id,
            expense_name,
            category,
            amount,
            expense_date,
            notes

        FROM expenses

        WHERE user_id = ?
        """,
        (user_id,)
    )

    expenses = cursor.fetchall()

    connection.close()

    expense_list = []

    for expense in expenses:

        expense_list.append({

            "expense_id": expense[0],
            "expense_name": expense[1],
            "category": expense[2],
            "amount": expense[3],
            "expense_date": expense[4],
            "notes": expense[5]

        })

    return jsonify(expense_list), 200


# ==========================
# Delete Expense
# ==========================
@expense_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def remove_expense(expense_id):

    # Logged-in user id
    user_id = get_jwt_identity()

    rows_deleted = delete_expense(expense_id, user_id)

    if rows_deleted == 0:

        return jsonify({
            "message": "Expense not found."
        }), 404

    return jsonify({
        "message": "Expense deleted successfully."
    }), 200

@expense_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
@jwt_required()
def edit_expense(expense_id):

    data = request.get_json()

    expense_name = data.get("expense_name")
    category = data.get("category")
    amount = data.get("amount")
    expense_date = data.get("expense_date")
    notes = data.get("notes")

    user_id = get_jwt_identity()

    rows_updated = update_expense(
        expense_id,
        user_id,
        expense_name,
        category,
        amount,
        expense_date,
        notes
    )

    if rows_updated == 0:

        return jsonify({
            "message": "Expense not found."
        }), 404

    return jsonify({
        "message": "Expense updated successfully."
    }), 200    