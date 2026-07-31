from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from db import (
    get_total_income,
    get_total_expenses,
    get_expense_category_summary,
    predict_monthly_expenses
)

load_dotenv()

ai_bp = Blueprint("ai", __name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@ai_bp.route("/ai/chat", methods=["POST"])
@jwt_required()
def ai_chat():

    data = request.get_json()

    message = data.get("message")

    if not message:

        return jsonify(
            {
                "message": "Message is required."
            }
        ), 400

    try:

        user_id = get_jwt_identity()

        # ==========================
        # Financial Data
        # ==========================

        total_income = get_total_income(user_id)

        total_expenses = get_total_expenses(user_id)

        balance = total_income - total_expenses

        predicted_monthly = predict_monthly_expenses(user_id)

        predicted_balance = total_income - predicted_monthly

        # ==========================
        # Purchase Amount Detection
        # ==========================

        purchase_amount = None

        match = re.search(r'(\d+(?:,\d+)*)', message)

        if match:

            purchase_amount = float(
                match.group(1).replace(",", "")
            )

        # ==========================
        # Financial Risk
        # ==========================

        if predicted_balance < 0:

            overspending = abs(predicted_balance)

            risk = "HIGH"

        elif predicted_balance < (total_income * 0.20):

            overspending = 0

            risk = "MEDIUM"

        else:

            overspending = 0

            risk = "LOW"

        # ==========================
        # Expense Categories
        # ==========================

        category_summary = get_expense_category_summary(user_id)

        category_text = ""

        highest_category = "None"

        highest_amount = 0

        if category_summary:

            for category, amount in category_summary:

                category_text += f"- {category}: Rs. {amount}\n"

                if amount > highest_amount:

                    highest_amount = amount

                    highest_category = category

        else:

            category_text = "No expenses recorded."

        # ==========================
        # Context for AI
        # ==========================

        financial_context = f"""
User Financial Information

Current Income:
Rs. {total_income}

Current Expenses:
Rs. {total_expenses}

Current Balance:
Rs. {balance}

Predicted Monthly Expenses:
Rs. {predicted_monthly}

Predicted Month-End Balance:
Rs. {predicted_balance}

Overspending Amount:
Rs. {overspending}

Financial Risk:
{risk}

Highest Spending Category:
{highest_category}

Expense Category Breakdown:

{category_text}

Proposed Purchase Amount:

Rs. {purchase_amount if purchase_amount else "Not Provided"}
"""

        # ==========================
        # OpenAI
        # ==========================

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content": """
You are an expert AI Financial Advisor.

Always analyze the user's financial data before answering.

Responsibilities:

- Analyze income and expenses.
- Predict future spending.
- Explain financial health.
- Mention the highest spending category.
- Give budgeting advice.
- Give saving suggestions.
- Predict whether the user may run out of money.

If the user asks whether they can buy something:

- Compare purchase amount with income.
- Compare purchase amount with balance.
- Compare purchase amount with predicted monthly expenses.
- Decide whether it is financially safe.
- Clearly answer YES or NO.
- Explain why.
- Give practical financial advice.

Never invent financial information.

Always answer ONLY using the provided financial data.
"""
                },

                {
                    "role": "system",
                    "content": financial_context
                },

                {
                    "role": "user",
                    "content": message
                }

            ]

        )

        return jsonify(
            {
                "reply": response.choices[0].message.content
            }
        ), 200

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify(
            {
                "error": str(e)
            }
        ), 500       