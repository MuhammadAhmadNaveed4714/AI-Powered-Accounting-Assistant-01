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
    get_system_total_expenses
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

    delete_income(income_id)

    return jsonify(
        {
            "message": "Income deleted successfully."
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


# ==============================
# AI PDF Report
# ==============================

@admin_bp.route("/admin/ai/report", methods=["GET"])
@jwt_required()
def admin_ai_report():

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
    "content": """
You are a professional financial analyst.

Generate a clean professional report.

Do NOT use Markdown.

Do NOT use **, ##, ---, bullet points, or tables.

Return plain text only.

Keep the report under 200 words.
"""
},

            {
                "role": "user",
                "content": f"""
Total Users: {total_users}

Total Admins: {total_admins}

Total Income: Rs. {total_income}

Total Expenses: Rs. {total_expenses}

Generate a professional report for the administrator.
"""
            }

        ]

    )

    ai_summary = response.choices[0].message.content

    file_name = "Admin_AI_Report.pdf"

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Accounting Assistant - Admin Report",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Total Users: {total_users}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Total Admins: {total_admins}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Total Income: Rs. {total_income}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Total Expenses: Rs. {total_expenses}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "AI Analysis",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            ai_summary,
            styles["Normal"]
        )
    )

    doc.build(story)

    return send_file(
        file_name,
        as_attachment=True
    )