from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="user")  

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self, include_password=False):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }
        if include_password:
            data["password"] = self.password
        # login sonrası kullanıcı yönlendirme sayfası için url ekle ("index.html" olarak)
        if self.role == "admin":
            data["redirect_url"] = "admin.html"
        else:
            data["redirect_url"] = "index.html"
        return data
