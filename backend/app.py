from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.ai import ai_bp
from routes.auth import auth_bp
from routes.expenses import expense_bp
from routes.income import income_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp
from routes.ai_report import ai_report_bp
from routes.documents import documents_bp

from db import create_tables

import os


app = Flask(__name__)

# =========================
# CORS
# =========================

CORS(app)


# =========================
# JWT Configuration
# =========================

app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    "my-secret-key"
)

jwt = JWTManager(app)


# =========================
# Database
# =========================

create_tables()


# =========================
# Register Blueprints
# =========================

app.register_blueprint(auth_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(income_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(ai_report_bp)
app.register_blueprint(documents_bp)


# =========================
# React Frontend
# =========================

FRONTEND_FOLDER = os.path.join(
    app.root_path,
    "frontend_build"
)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):

    requested_file = os.path.join(
        FRONTEND_FOLDER,
        path
    )

    # Serve requested static file
    if path and os.path.exists(requested_file):
        return send_from_directory(
            FRONTEND_FOLDER,
            path
        )

    # React SPA fallback
    index_file = os.path.join(
        FRONTEND_FOLDER,
        "index.html"
    )

    if os.path.exists(index_file):
        return send_from_directory(
            FRONTEND_FOLDER,
            "index.html"
        )

    return {
        "error": "Frontend build not found",
        "frontend_folder": FRONTEND_FOLDER
    }, 500


# =========================
# Uploaded Files
# =========================

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.route("/uploads/<filename>")
def serve_uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# =========================
# Start Flask Server
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                8080
            )
        )
    )