import os
from urllib.parse import quote_plus

# Sizin özel veritabanı bilgileriniz (image_34c332.png baz alınarak)
DB_USER = 'root'
DB_PASS = quote_plus('Asdasd123!!')
DB_HOST = 'localhost'
DB_NAME = 'akillikutuphane'

class Config:
    # Genel Ayarlar
    SECRET_KEY = 'Asdasd123!!'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'Asdasd123!!'

    # Mail Ayarları (image_34c332.png'deki bilgileriniz)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bacaksizaliberk021@gmail.com'
    MAIL_PASSWORD = 'ippmlorjpwuppuia'
    MAIL_DEFAULT_SENDER = 'bacaksizaliberk021@gmail.com'

# Uygulamanızın DevelopmentConfig beklentisini karşılamak için:
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# __init__.py içindeki create_app() için gerekli sözlük yapısı
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}