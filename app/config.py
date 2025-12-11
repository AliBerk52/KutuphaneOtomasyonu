from urllib.parse import quote_plus

DB_USER = 'root'
DB_PASS = quote_plus('Asdasd123!!')  
DB_HOST = 'localhost'
DB_NAME = 'kutuphaneler'

class Config:

    SECRET_KEY = 'Asdasd123!!'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

        # 🔹 MAIL AYARLARI (Gmail)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bacaksizaliberk021@gmail.com'
    MAIL_PASSWORD = 'ippmlorjpwuppuia'
    MAIL_DEFAULT_SENDER = 'bacaksizaliberk021@gmail.com'