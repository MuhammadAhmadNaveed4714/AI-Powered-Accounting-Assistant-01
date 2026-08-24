from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

import os
import json

from db import (
    create_document,
    get_documents_by_user,
    create_receipt,
    create_bill,
    get_receipts_by_user,
    get_bills_by_user
)

from ai.pdf_reader import extract_text_from_pdf
from ai.ocr import extract_text_from_image
from ai.extractor import extract_document_data


documents_bp = Blueprint("documents", __name__)


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# Upload Document
# =========================================================

@documents_bp.route("/documents/upload", methods=["POST"])
@jwt_required()
def upload_document():

    user_id = get_jwt_identity()


    # =========================
    # Check File
    # =========================

    if "file" not in request.files:

        return jsonify({
            "message": "No file selected"
        }), 400


    file = request.files["file"]


    if file.filename == "":

        return jsonify({
            "message": "No file selected"
        }), 400


    # =========================
    # Get Document Type
    # =========================

    document_type = request.form.get("document_type")


    if not document_type:

        return jsonify({
            "message": "Document type is required"
        }), 400


    document_type = document_type.lower().strip()


    # =========================
    # Only Bill and Receipt
    # =========================

    if document_type not in ["bill", "receipt"]:

        return jsonify({
            "message": "Only Bill and Receipt documents are supported"
        }), 400


    # =========================
    # Save File
    # =========================

    filename = secure_filename(file.filename)


    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    file.save(filepath)


    # =========================
    # OCR / PDF Extraction
    # =========================

    extension = filename.lower().split(".")[-1]


    if extension in ["jpg", "jpeg", "png"]:

        extracted_text, cleaned_text = extract_text_from_image(
            filepath
        )

    else:

        extracted_text = extract_text_from_pdf(filepath)

        cleaned_text = extracted_text


    # =========================
    # Print OCR
    # =========================



    # =========================
    # AI Extraction
    # =========================

    try:

        ai_result = extract_document_data(
            document_type,
            cleaned_text
        )

    except Exception as e:

        print("AI Extraction Error:", e)

        return jsonify({
            "message": "AI extraction failed",
            "error": str(e)
        }), 500


    print("\n========== AI RESULT ==========\n")
    print(ai_result)
    print("\n===============================\n")


    # =========================
    # Convert AI JSON
    # =========================

    if isinstance(ai_result, str):

        try:

            ai_result = json.loads(
                ai_result
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        except json.JSONDecodeError:

            return jsonify({
                "message": "AI returned invalid JSON",
                "ai_result": ai_result
            }), 500


    # =========================
    # Save Document
    # =========================

    document_id = create_document(

        user_id,

        document_type,

        filename,

        filepath,

        extracted_text,

        cleaned_text,

        json.dumps(ai_result)

    )


    # =====================================================
    # Save Receipt
    # =====================================================

    if document_type == "receipt":

        create_receipt(

            user_id,

            document_id,

            ai_result.get("amount"),

            ai_result.get("receiver"),

            ai_result.get("sender"),

            ai_result.get("transaction_id"),

            ai_result.get("transaction_date")

        )


    # =====================================================
    # Save Bill
    # =====================================================

    elif document_type == "bill":

        create_bill(

            user_id,

            document_id,

            ai_result.get("name"),

            ai_result.get("issue_date"),

            ai_result.get("bill_month"),

            ai_result.get("due_date"),

            ai_result.get("reference_no"),

            ai_result.get("payable_within_due_date"),

            ai_result.get("payable_after_due_date")

        )


    # =========================
    # Response
    # =========================

    return jsonify({

        "message": "Document uploaded successfully!",

        "document_id": document_id,

        "document_type": document_type,

        "ai_result": ai_result

    }), 200


# =========================================================
# Get User Documents
# =========================================================

@documents_bp.route("/documents", methods=["GET"])
@jwt_required()
def get_documents():

    user_id = get_jwt_identity()


    documents = get_documents_by_user(user_id)


    return jsonify(documents), 200



@documents_bp.route("/receipts", methods=["GET"])
@jwt_required()
def get_receipts():

    user_id = get_jwt_identity()

    receipts = get_receipts_by_user(user_id)

    return jsonify(receipts), 200


@documents_bp.route("/bills", methods=["GET"])
@jwt_required()
def get_bills():

    user_id = get_jwt_identity()

    bills = get_bills_by_user(user_id)

    return jsonify(bills), 200    
