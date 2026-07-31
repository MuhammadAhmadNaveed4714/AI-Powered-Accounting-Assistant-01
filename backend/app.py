from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.ai import ai_bp
from db import create_tables
from routes.auth import auth_bp
from routes.expenses import expense_bp
from routes.income import income_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp
from routes.ai_report import ai_report_bp
app = Flask(__name__)


# Allow React frontend connection
CORS(app)


# JWT Configuration
app.config["JWT_SECRET_KEY"] = "my-secret-key"

jwt = JWTManager(app)


# Create database tables
create_tables()


# Register Routes
app.register_blueprint(auth_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(income_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(ai_report_bp)
@app.route("/")
def home():

    return {
        "message": "Backend is running successfully!"
    }



if __name__ == "__main__":

    app.run(debug=True)