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

from ai.ocr import extract_text_from_image
from ai.extractor import extract_document_data


documents_bp = Blueprint("documents", __name__)


# =========================================================
# Upload Configuration
# =========================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


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
    # Check File Type
    # =========================

    if not allowed_file(file.filename):
        return jsonify({
            "message": "Only JPG, JPEG and PNG images are supported"
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
    # Secure Filename
    # =========================

    filename = secure_filename(file.filename)

    if not filename:
        return jsonify({
            "message": "Invalid filename"
        }), 400

    # =========================
    # Create Unique Filename
    # =========================

    name, extension = os.path.splitext(filename)

    filename = f"{user_id}_{name}{extension.lower()}"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    # =========================
    # Save Image
    # =========================

    try:

        file.save(filepath)

    except Exception as e:

        print("File Save Error:", e, flush=True)

        return jsonify({
            "message": "Failed to save uploaded file",
            "error": str(e)
        }), 500

    # =========================
    # OCR Extraction
    # =========================

    try:

        print(
            f"OCR: Processing {filename}",
            flush=True
        )

        extracted_text, cleaned_text = extract_text_from_image(
            filepath
        )

        print(
            "OCR: Image processing completed",
            flush=True
        )

    except Exception as e:

        print(
            "OCR Processing Error:",
            e,
            flush=True
        )

        return jsonify({
            "message": "OCR processing failed",
            "error": str(e)
        }), 500

    # =========================
    # Check OCR Result
    # =========================

    if not cleaned_text or not cleaned_text.strip():

        return jsonify({
            "message": "Could not extract text from the image",
            "error": "OCR returned empty text"
        }), 400

    # =========================
    # AI Extraction
    # =========================

    try:

        ai_result = extract_document_data(
            document_type,
            cleaned_text
        )

    except Exception as e:

        print(
            "AI Extraction Error:",
            e,
            flush=True
        )

        return jsonify({
            "message": "AI extraction failed",
            "error": str(e)
        }), 500

    # =========================
    # Print AI Result
    # =========================

    print(
        "\n========== AI RESULT ==========\n",
        flush=True
    )

    print(
        ai_result,
        flush=True
    )

    print(
        "\n===============================\n",
        flush=True
    )

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
    # Make Sure AI Result is Dict
    # =========================

    if not isinstance(ai_result, dict):

        return jsonify({
            "message": "AI returned an invalid response"
        }), 500

    # =========================
    # Save Document
    # =========================

    try:

        document_id = create_document(

            user_id,

            document_type,

            filename,

            filepath,

            extracted_text,

            cleaned_text,

            json.dumps(ai_result)

        )

    except Exception as e:

        print(
            "Database Document Error:",
            e,
            flush=True
        )

        return jsonify({
            "message": "Failed to save document",
            "error": str(e)
        }), 500

    # =========================================================
    # Save Receipt
    # =========================================================

    if document_type == "receipt":

        try:

            create_receipt(

                user_id,

                document_id,

                ai_result.get("amount"),

                ai_result.get("receiver"),

                ai_result.get("sender"),

                ai_result.get("transaction_id"),

                ai_result.get("transaction_date")

            )

        except Exception as e:

            print(
                "Receipt Database Error:",
                e,
                flush=True
            )

            return jsonify({
                "message": "Document saved but receipt data could not be saved",
                "error": str(e)
            }), 500

    # =========================================================
    # Save Bill
    # =========================================================

    elif document_type == "bill":

        try:

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

        except Exception as e:

            print(
                "Bill Database Error:",
                e,
                flush=True
            )

            return jsonify({
                "message": "Document saved but bill data could not be saved",
                "error": str(e)
            }), 500

    # =========================
    # Response
    # =========================

    return jsonify({

        "message": "Document uploaded successfully!",

        "document_id": document_id,

        "document_type": document_type,

        "filename": filename,

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


# =========================================================
# Get User Receipts
# =========================================================

@documents_bp.route("/receipts", methods=["GET"])
@jwt_required()
def get_receipts():

    user_id = get_jwt_identity()

    receipts = get_receipts_by_user(user_id)

    return jsonify(receipts), 200


# =========================================================
# Get User Bills
# =========================================================

@documents_bp.route("/bills", methods=["GET"])
@jwt_required()
def get_bills():

    user_id = get_jwt_identity()

    bills = get_bills_by_user(user_id)

    return jsonify(bills), 200