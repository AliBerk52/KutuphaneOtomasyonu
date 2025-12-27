from app import db, bcrypt, jwt
from app.models import User
from app.repositories.user_repository import UserRepository 
# NOT: user_repository.py'yi henüz oluşturmadık, ancak import edebiliriz.
# Eğer bu dosyayı daha sonra oluşturursak hata almayız.
from flask_jwt_extended import create_access_token

class UserService:
    
    @staticmethod
    def register_user(username, email, password, role='user'):
        """Yeni bir kullanıcıyı kaydeder ve şifresini hash'ler."""
        if UserRepository.get_user_by_email(email):
            return {"success": False, "message": "Bu e-posta adresi zaten kullanımda."}
        
        # Şifreyi hash'le
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Kullanıcı oluşturma
        new_user = User(
            username=username, 
            email=email, 
            password_hash=hashed_password, 
            role=role
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return {"success": True, "user": new_user}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Kayıt işlemi sırasında bir hata oluştu: {str(e)}"}

    @staticmethod
    def authenticate_user(email, password):
        """Kullanıcıyı doğrular ve başarılı olursa JWT token üretir."""
        user = UserRepository.get_user_by_email(email)
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Şifre doğru, JWT token oluştur
            
            # Token içine user_id, email ve role bilgisini ekliyoruz (payload)
            access_token = create_access_token(identity=str(user.id), 
                                               additional_claims={'email': user.email, 'role': user.role})
            
            return {
                "success": True, 
                "message": "Giriş başarılı.", 
                "user_id": user.id,
                "role": user.role,
                "token": access_token
            }
        
        return {"success": False, "message": "Geçersiz e-posta veya şifre."}

    @staticmethod
    def is_admin(user_id):
        """Kullanıcının yönetici yetkisine sahip olup olmadığını kontrol eder."""
        user = UserRepository.get_user_by_id(user_id)
        return user and user.role == 'admin'

    # Diğer kullanıcı yönetimi fonksiyonları (şifre sıfırlama, profil güncelleme vb.) buraya eklenebilir.