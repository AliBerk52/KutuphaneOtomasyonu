import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# --- Uzantı Nesnelerinin Tanımlanması ---
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='development'):
    app = Flask(__name__)

    # 1. Konfigürasyonu Yükle (app/config.py dosyasından)
    from app.config import config
    app.config.from_object(config[config_name])

    # 2. Uzantıları Uygulamaya Bağla
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 3. JWT Kimlik Yapılandırması (User modeline göre)
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        # User nesnesi gelirse ID'sini, ID gelirse direkt kendisini döner
        return user.id if hasattr(user, 'id') else user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from app.models.user import User
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    # 4. Blueprint (Controller) Kayıtları
    with app.app_context():
        # User Controller (Kayıt ve Giriş işlemleri /api/v1/auth altında)
        from app.controllers.user_controller import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/v1/auth')

        # Book Controller (Kitap Arama ve Liste)
        from app.controllers.book_controller import book_bp
        app.register_blueprint(book_bp, url_prefix='/api/v1/books')
        
        # Loan Controller (Ödünç Alma, İade ve Admin Takip)
        from app.controllers.loan_controller import loan_bp
        app.register_blueprint(loan_bp, url_prefix='/api/v1/loans')
        
        # Admin Controller (Kategori ve Yazar CRUD)
        from app.controllers.admin_controller import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

        # Main Controller (Sayfa yönlendirmeleri: /login, /register, /dashboard)
        from app.controllers.main_controller import main_bp
        app.register_blueprint(main_bp)

        # Tabloları oluştur (Eğer yoksa)
        db.create_all()

    return app