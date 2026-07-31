from flask import Blueprint, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


from db import (
    get_total_income,
    get_total_expenses,
    get_expense_by_category
)

from openai import OpenAI



ai_report_bp = Blueprint(
    "ai_report",
    __name__
)



@ai_report_bp.route(
    "/ai/report",
    methods=["GET"]
)
@jwt_required()
def generate_ai_report():


    user_id = get_jwt_identity()


    # Get financial data

    total_income = get_total_income(
        user_id
    )


    total_expenses = get_total_expenses(
        user_id
    )


    balance = total_income - total_expenses


    categories = get_expense_by_category(
        user_id
    )



    # OpenAI

    client = OpenAI()


    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",
                "content":
                "You are a professional financial advisor. Give short and useful financial advice."
            },


            {
                "role": "user",

                "content": f"""

Analyze this user's financial data:

Total Income:
Rs. {total_income}


Total Expenses:
Rs. {total_expenses}


Balance:
Rs. {balance}


Expense Categories:
{categories}


Generate a professional financial summary with suggestions.

"""
            }

        ]

    )


    ai_summary = response.choices[0].message.content



    # Create PDF

    file_name = "AI_Financial_Report.pdf"


    doc = SimpleDocTemplate(
        file_name
    )


    styles = getSampleStyleSheet()


    content = []



    content.append(

        Paragraph(
            "AI Accounting Assistant Financial Report",
            styles["Heading2"]
        )

    )


    content.append(
        Spacer(1,20)
    )



    content.append(

        Paragraph(
            f"Total Income: Rs. {total_income}",
            styles["Normal"]
        )

    )


    content.append(

        Paragraph(
            f"Total Expenses: Rs. {total_expenses}",
            styles["Normal"]
        )

    )


    content.append(

        Paragraph(
            f"Balance: Rs. {balance}",
            styles["Normal"]
        )

    )



    content.append(
        Spacer(1,20)
    )



    content.append(

        Paragraph(
            "AI Financial Analysis:",
            styles["Heading3"]
        )

    )


    content.append(

        Paragraph(
            ai_summary,
            styles["Normal"]
        )

    )



    doc.build(content)


    return send_file(
        file_name,
        as_attachment=True
    )   