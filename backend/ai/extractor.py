import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_document_data(document_type, pdf_text):

    # =====================================================
    # RECEIPT PROMPT
    # =====================================================

    receipt_prompt = f"""
You are an expert AI Accounting Assistant.

Extract structured information from the receipt below.

The text was extracted using OCR, so some characters may be incorrect.

Common OCR mistakes include:

S125 -> $125
S250 -> $250
S50 -> $50
sso -> $50
S550 -> $550
5s0 -> 550
0oo123 -> 000123

Correct only obvious OCR mistakes using the surrounding context.

IMPORTANT RECEIPT RULES:

1. "amount" means the actual amount paid/received.

2. "amount" must be a NUMBER only.

Example:
1190.00

Do NOT return:
"$1,190.00"
"Rs. 1,190.00"

3. "receiver" means the person/company mentioned after:
To
Receiver
Paid To

4. "sender" means the person/company mentioned after:
From
Sender
Paid By

5. "transaction_id" means the transaction/reference ID.

For example:

TID: 719289997097

Then:

"transaction_id": "719289997097"

DO NOT use the amount as transaction_id.

6. "transaction_date" must be returned in:

YYYY-MM-DD

Example:

01 Aug 2026 -> 2026-08-01

7. If a field is missing, return null.

8. Do NOT invent information.

9. Return ONLY valid JSON.

10. Do NOT return markdown.

11. Do NOT use ```json.

JSON:

{{
    "amount": null,
    "receiver": null,
    "sender": null,
    "transaction_id": null,
    "transaction_date": null
}}

Receipt Text:

{pdf_text}
"""


    # =====================================================
    # BILL PROMPT
    # =====================================================

    bill_prompt = f"""
You are an expert AI Accounting Assistant.

Extract structured information from the bill below.

The text was extracted using OCR, so some characters may be incorrect.

Common OCR mistakes include:

S125 -> $125
S250 -> $250
S50 -> $50
sso -> $50
S550 -> $550
5s0 -> 550
0oo123 -> 000123

Correct only obvious OCR mistakes using the surrounding context.

IMPORTANT BILL RULES:

1. "name" means the company, organization, utility provider,
or person that issued the bill.

2. "issue_date" must be returned in:

YYYY-MM-DD

3. "bill_month" should contain the billing month.

Example:

July 2026

4. "due_date" must be returned in:

YYYY-MM-DD

5. "reference_no" means the bill/reference/account/reference number.

6. "payable_within_due_date" means the amount that must be paid
if payment is made on or before the due date.

It must be a NUMBER only.

Example:

1500.00

7. "payable_after_due_date" means the amount that must be paid
if payment is made after the due date.

It must be a NUMBER only.

Example:

1700.00

8. Do NOT include currency symbols such as:
$
Rs.
PKR

in monetary values.

9. Correct obvious OCR mistakes in monetary values.

10. If a field is missing, return null.

11. Do NOT invent information.

12. Return ONLY valid JSON.

13. Do NOT return markdown.

14. Do NOT use ```json.

JSON:

{{
    "name": null,
    "issue_date": null,
    "bill_month": null,
    "due_date": null,
    "reference_no": null,
    "payable_within_due_date": null,
    "payable_after_due_date": null
}}

Bill Text:

{pdf_text}
"""


    # =====================================================
    # SELECT PROMPT
    # =====================================================

    document_type = document_type.lower().strip()


    if document_type == "receipt":

        prompt = receipt_prompt

    elif document_type == "bill":

        prompt = bill_prompt

    else:

        raise ValueError(
            "Unsupported document type. Only 'receipt' and 'bill' are supported."
        )


    # =====================================================
    # OPENAI REQUEST
    # =====================================================

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )


    return response.output_text

