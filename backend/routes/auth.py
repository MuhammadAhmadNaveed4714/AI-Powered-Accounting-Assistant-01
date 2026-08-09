from flask import Blueprint, request, jsonify
import bcrypt
from flask_jwt_extended import create_access_token

from db import (
    get_user_by_email,
    create_user,
    get_connection
)


auth_bp = Blueprint("auth", __name__)


# =========================================================
# Register
# =========================================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")


    # =========================
    # Validate Input
    # =========================

    if not username or not email or not password:

        return jsonify({
            "message": "All fields are required."
        }), 400


    # =========================
    # Check Existing Email
    # =========================

    if get_user_by_email(email):

        return jsonify({
            "message": "Email already exists."
        }), 400


    # =========================
    # Determine Role
    # =========================

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE role = 'admin'"
    )


    admin_count = cursor.fetchone()[0]


    connection.close()


    # First registered account = Admin
    if admin_count == 0:

        role = "admin"

    else:

        role = "user"


    # =========================
    # Hash Password
    # =========================

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


    # =========================
    # Save User
    # =========================

    create_user(
        username,
        email,
        hashed_password,
        role
    )


    # =========================
    # Response
    # =========================

    if role == "admin":

        message = "Admin account created successfully."

    else:

        message = "User registered successfully."


    return jsonify({
        "message": message,
        "role": role
    }), 201


# =========================================================
# Login
# =========================================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")


    # =========================
    # Validate Input
    # =========================

    if not email or not password:

        return jsonify({
            "message": "Email and password are required."
        }), 400


    # =========================
    # Find User
    # =========================

    user = get_user_by_email(email)


    if not user:

        return jsonify({
            "message": "Invalid email or password."
        }), 401


    # =========================
    # Verify Password
    # =========================

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user[3].encode("utf-8")
    ):

        return jsonify({
            "message": "Invalid email or password."
        }), 401


    # =========================
    # Create JWT Token
    # =========================

    access_token = create_access_token(
        identity=str(user[0])
    )


    # =========================
    # Response
    # =========================

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
