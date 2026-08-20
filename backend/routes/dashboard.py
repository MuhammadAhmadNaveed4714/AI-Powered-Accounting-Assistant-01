from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from openai import OpenAI

from db import (
    get_total_income,
    get_total_expenses,
    get_expense_categories,
    get_monthly_summary
)

dashboard_bp = Blueprint("dashboard", __name__)


# =========================================================
# USER DASHBOARD
# =========================================================

@dashboard_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():

    user_id = int(get_jwt_identity())

    date_filter = request.args.get("filter", "all")

    total_income = get_total_income(
        user_id,
        date_filter
    )

    total_expenses = get_total_expenses(
        user_id,
        date_filter
    )

    balance = total_income - total_expenses

    category_data = get_expense_categories(
        user_id,
        date_filter
    )

    monthly_summary = get_monthly_summary(
        user_id,
        date_filter
    )

    categories = []

    for category, total in category_data:

        categories.append(
            {
                "category": category,
                "total": total
            }
        )

    # =====================================================
    # AI Financial Insight
    # =====================================================

    if total_income == 0:

        insight = (
            "No income recorded yet. "
            "Add your income to view financial insights."
        )

    elif balance < 0:

        insight = (
            "Warning! Your expenses are higher "
            "than your income."
        )

    elif total_expenses > (total_income * 0.8):

        insight = (
            "Your expenses are above 80% of your income. "
            "Consider reducing unnecessary spending."
        )

    elif total_expenses > (total_income * 0.5):

        insight = (
            "You are spending more than half of your income. "
            "Monitor your budget carefully."
        )

    else:

        insight = (
            "Great job! Your expenses are under control "
            "and your savings look healthy."
        )

    # =====================================================
    # AI Recommendation
    # =====================================================

    if balance < 0:

        recommendation = (
            "Reduce your expenses immediately "
            "and avoid unnecessary purchases."
        )

    elif total_expenses > (total_income * 0.8):

        recommendation = (
            "Aim to reduce your expenses below "
            "80% of your income."
        )

    elif total_expenses > (total_income * 0.5):

        recommendation = (
            "Try to save at least 20% "
            "of your monthly income."
        )

    else:

        recommendation = (
            "Excellent financial management! "
            "Continue saving regularly."
        )

    return jsonify(
        {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "insight": insight,
            "recommendation": recommendation,
            "categories": categories,
            "monthly_summary": monthly_summary
        }
    ), 200


# =========================================================
# AI FINANCIAL SUMMARY
# =========================================================

@dashboard_bp.route(
    "/dashboard/ai-summary",
    methods=["GET"]
)
@jwt_required()
def dashboard_ai_summary():

    try:

        # -------------------------------------------------
        # Get logged-in user
        # -------------------------------------------------

        user_id = int(get_jwt_identity())

        # -------------------------------------------------
        # Get selected date filter
        # -------------------------------------------------

        date_filter = request.args.get(
            "filter",
            "all"
        )

        # -------------------------------------------------
        # Get user's financial data
        # -------------------------------------------------

        total_income = get_total_income(
            user_id,
            date_filter
        )

        total_expenses = get_total_expenses(
            user_id,
            date_filter
        )

        balance = total_income - total_expenses

        # -------------------------------------------------
        # OpenAI
        # -------------------------------------------------

        client = OpenAI()

        ai_response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a professional personal financial analyst.

Analyze the user's financial data and provide a
short, clear and useful financial analysis.

Do NOT use Markdown.

Do NOT use bullet points.

Do NOT use headings with # symbols.

Keep the response professional and easy to understand.

The analysis should discuss:

1. Current financial situation
2. Spending behavior
3. Savings or balance situation
4. One practical recommendation

Keep the analysis under 150 words.
"""
                },

                {
                    "role": "user",

                    "content": f"""
Financial Period: {date_filter}

Total Income: Rs. {total_income}

Total Expenses: Rs. {total_expenses}

Current Balance: Rs. {balance}

Analyze the user's financial situation and
provide a useful financial summary.
"""
                }

            ]

        )

        # -------------------------------------------------
        # Get AI response
        # -------------------------------------------------

        ai_summary = (
            ai_response
            .choices[0]
            .message
            .content
        )

        # -------------------------------------------------
        # Return response with NO-CACHE headers
        # -------------------------------------------------

        result = jsonify(
            {
                "ai_summary": ai_summary
            }
        )

        result.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )

        result.headers["Pragma"] = "no-cache"

        result.headers["Expires"] = "0"

        return result, 200

    except Exception as error:

        print(
            "AI SUMMARY ERROR:",
            error
        )

        return jsonify(
            {
                "message": "Failed to generate AI summary."
            }
        ), 500