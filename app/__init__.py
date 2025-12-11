import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from app.config import Config



db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)

    # 🔥 Proje ana dizinini bul
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # app klasörünün yolu
    PROJECT_ROOT = os.path.dirname(BASE_DIR)                # AkıllıKutuphane/
    FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")   # AkıllıKutuphane/frontend

    # ----------------------------------------------------------------------------------------
    # FRONTEND SERVE: http://127.0.0.1:5000 → index.html
    # ----------------------------------------------------------------------------------------
    @app.route('/')
    def serve_frontend():
        return send_from_directory(FRONTEND_DIR, 'index.html')

    # Diğer statik dosyaları da yükleyebilmek için:
    @app.route('/<path:path>')
    def serve_static_files(path):
        return send_from_directory(FRONTEND_DIR, path)

    # ----------------------------------------------------------------------------------------
    with app.app_context():
        from .models import user, book, author, category, borrow
        from .controllers.user_controller import user_bp
        from .controllers.book_controller import book_bp

        app.register_blueprint(user_bp)
        app.register_blueprint(book_bp)

        db.create_all()

    return app
