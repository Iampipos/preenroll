from flask import Flask, redirect, url_for
from config import *
from models import db
from controllers.auth import bp as auth_bp
from controllers.admin import bp as admin_bp
from controllers.student import bp as student_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)