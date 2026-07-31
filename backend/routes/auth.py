from flask import Blueprint, request, jsonify
import bcrypt
from flask_jwt_extended import create_access_token

from db import get_user_by_email, create_user


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")


    # Validate input
    if not username or not email or not password:
        return jsonify({
            "message": "All fields are required."
        }), 400


    # Check if email already exists
    if get_user_by_email(email):
        return jsonify({
            "message": "Email already exists."
        }), 400


    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


    # Save user
    create_user(
        username,
        email,
        hashed_password,
        "user"
    )


    return jsonify({
        "message": "User registered successfully."
    }), 201



@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")


    # Validate input
    if not email or not password:
        return jsonify({
            "message": "Email and password are required."
        }), 400


    # Find user by email
    user = get_user_by_email(email)


    if not user:
        return jsonify({
            "message": "Invalid email or password."
        }), 401


    # Verify password
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user[3].encode("utf-8")
    ):
        return jsonify({
            "message": "Invalid email or password."
        }), 401



        # Create JWT Token
    access_token = create_access_token(
        identity=str(user[0])
    )

    return jsonify({

        "message": "Login successful.",

        "access_token": access_token,

        "user": {
            "user_id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[4]
        }

    }), 200