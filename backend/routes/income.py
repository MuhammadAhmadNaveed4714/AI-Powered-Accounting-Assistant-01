from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import (
    add_income,
    get_user_income,
    get_all_income,
    delete_income,
    update_income
)
income_bp = Blueprint("income", __name__)
@income_bp.route("/income", methods=["POST"])
@jwt_required()
def create_income():

    user_id = get_jwt_identity()

    data = request.get_json()

    income_source = data.get("income_source")
    amount = data.get("amount")
    income_date = data.get("income_date")
    notes = data.get("notes")

    if not income_source or not amount or not income_date:

        return jsonify({
            "message": "Please fill all required fields."
        }), 400

    add_income(
        user_id,
        income_source,
        amount,
        income_date,
        notes
    )

    return jsonify({
        "message": "Income added successfully."
    }), 201

@income_bp.route("/income", methods=["GET"])
@jwt_required()
def get_income():

    user_id = get_jwt_identity()

    incomes = get_user_income(user_id)
    income_list = []

    for income in incomes:

        income_list.append({

            "income_id": income[0],
            "income_source": income[1],
            "amount": income[2],
            "income_date": income[3],
            "notes": income[4]

        })

    return jsonify(income_list), 200    

@income_bp.route("/income/<int:income_id>", methods=["DELETE"])
@jwt_required()
def remove_income(income_id):

    user_id = get_jwt_identity()

    rows_deleted = delete_income(
        income_id,
        user_id
    )

    if rows_deleted == 0:

        return jsonify({
            "message": "Income not found."
        }), 404

    return jsonify({
        "message": "Income deleted successfully."
    }), 200    

@income_bp.route("/income/<int:income_id>", methods=["PUT"])
@jwt_required()
def edit_income(income_id):

    user_id = get_jwt_identity()

    data = request.get_json()

    income_source = data.get("income_source")
    amount = data.get("amount")
    income_date = data.get("income_date")
    notes = data.get("notes")

    if not income_source or not amount or not income_date:

        return jsonify({
            "message": "Please fill all required fields."
        }), 400

    rows_updated = update_income(
        income_id,
        user_id,
        income_source,
        amount,
        income_date,
        notes
    )

    if rows_updated == 0:

        return jsonify({
            "message": "Income not found."
        }), 404

    return jsonify({
        "message": "Income updated successfully."
    }), 200

    