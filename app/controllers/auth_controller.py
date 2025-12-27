from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # E-posta kontrolü
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Bu e-posta zaten kullanımda."}), 400
    
    # Yeni kullanıcı oluştur (Default rol: user)
    new_user = User(username=data['username'], email=data['email'])
    # Şifreyi hashleyerek set et
    new_user.set_password(data['password']) 
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Kayıt başarılı"}), 201