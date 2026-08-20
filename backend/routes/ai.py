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


# =========================================================
# OPENAI CLIENT
# =========================================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================================================
# AI CHAT
# =========================================================

@ai_bp.route("/ai/chat", methods=["POST"])
@jwt_required()
def ai_chat():

    data = request.get_json()

    if not data:

        return jsonify(
            {
                "message": "Request data is required."
            }
        ), 400

    message = data.get("message")

    if not message or not message.strip():

        return jsonify(
            {
                "message": "Message is required."
            }
        ), 400

    try:

        # =================================================
        # GET LOGGED-IN USER
        # =================================================

        user_id = int(get_jwt_identity())


        # =================================================
        # FINANCIAL DATA
        # =================================================

        total_income = get_total_income(user_id)

        total_expenses = get_total_expenses(user_id)

        balance = total_income - total_expenses

        predicted_monthly = predict_monthly_expenses(user_id)

        predicted_balance = (
            total_income - predicted_monthly
        )


        # =================================================
        # PURCHASE AMOUNT DETECTION
        # =================================================

        purchase_amount = None

        match = re.search(
            r'(\d+(?:,\d+)*)',
            message
        )

        if match:

            purchase_amount = float(
                match.group(1).replace(",", "")
            )


        # =================================================
        # FINANCIAL RISK
        # =================================================

        if predicted_balance < 0:

            overspending = abs(
                predicted_balance
            )

            risk = "HIGH"

        elif (
            total_income > 0
            and predicted_balance < (total_income * 0.20)
        ):

            overspending = 0

            risk = "MEDIUM"

        else:

            overspending = 0

            risk = "LOW"


        # =================================================
        # EXPENSE CATEGORIES
        # =================================================

        category_summary = (
            get_expense_category_summary(user_id)
        )

        category_text = ""

        highest_category = "None"

        highest_amount = 0


        if category_summary:

            for category, amount in category_summary:

                category_text += (
                    f"- {category}: Rs. {amount}\n"
                )

                if amount > highest_amount:

                    highest_amount = amount

                    highest_category = category

        else:

            category_text = (
                "No expenses recorded."
            )


        # =================================================
        # FINANCIAL CONTEXT
        # =================================================

        financial_context = f"""
USER FINANCIAL INFORMATION

Total Income:
Rs. {total_income}

Total Expenses:
Rs. {total_expenses}

Current Balance:
Rs. {balance}

Predicted Monthly Expenses:
Rs. {predicted_monthly}

Predicted Month-End Balance:
Rs. {predicted_balance}

Potential Overspending:
Rs. {overspending}

Financial Risk:
{risk}

Highest Spending Category:
{highest_category}

Expense Category Breakdown:

{category_text}

Proposed Purchase Amount:
Rs. {purchase_amount if purchase_amount is not None else "Not Provided"}
"""


        # =================================================
        # OPENAI REQUEST
        # =================================================

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a professional AI Financial Assistant.

Analyze the user's financial information before answering.

IMPORTANT RULES:

1. Use ONLY the financial information provided.
2. Never invent income, expenses, balances or transactions.
3. Keep answers short, clear and easy to understand.
4. Avoid unnecessary explanations.
5. Do not use tables.
6. Avoid complicated financial terminology.
7. Use short paragraphs.
8. Use simple bullet points when helpful.
9. Give practical and realistic financial advice.
10. Do not repeat the entire financial context.

When discussing financial health, consider:

- Income
- Expenses
- Current balance
- Predicted monthly expenses
- Predicted month-end balance
- Financial risk
- Highest spending category

If the user asks whether they can afford a purchase:

- Clearly answer YES or NO.
- Compare the purchase amount with their current balance.
- Consider predicted monthly expenses.
- Explain the reason briefly.
- Give one practical recommendation.

RESPONSE STYLE:

Keep the response under 120 words.

Use this structure when appropriate:

💡 Conclusion:
Give the main answer in 1-2 sentences.

📊 Financial Insight:
Briefly explain the relevant financial situation.

💰 Recommendation:
Give one practical recommendation.

Do not use # headings.
Do not write long paragraphs.
Do not repeat information unnecessarily.
"""
                },

                {
                    "role": "system",

                    "content": financial_context
                },

                {
                    "role": "user",

                    "content": message.strip()
                }

            ],

            temperature=0.4,

            max_tokens=250

        )


        # =================================================
        # GET AI RESPONSE
        # =================================================

        ai_reply = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )


        # =================================================
        # RETURN RESPONSE
        # =================================================

        return jsonify(
            {
                "reply": ai_reply
            }
        ), 200


    except Exception as error:

        import traceback

        print(
            "========================================"
        )

        print(
            "AI CHAT ERROR:"
        )

        print(
            str(error)
        )

        traceback.print_exc()

        print(
            "========================================"
        )


        return jsonify(
            {
                "message": (
                    "Failed to generate AI response."
                ),

                "error": str(error)
            }
        ), 500