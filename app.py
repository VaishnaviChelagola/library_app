from flask import Flask
from auth import auth_bp
from admin import admin_bp
from member import member_bp
from database import init_db

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(member_bp, url_prefix="/member")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
