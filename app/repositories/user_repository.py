from app import db
from app.models import User

class UserRepository:
    
    @staticmethod
    def get_user_by_id(user_id):
        """ID'ye göre kullanıcıyı getirir."""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        """E-posta adresine göre kullanıcıyı getirir."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username):
        """Kullanıcı adına göre kullanıcıyı getirir."""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def update_user_role(user_id, new_role):
        """Kullanıcının rolünü günceller (Admin işlemleri için)."""
        user = UserRepository.get_user_by_id(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            return user
        return None
        
    @staticmethod
    def delete_user(user_id):
        """Kullanıcıyı siler."""
        user = UserRepository.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False