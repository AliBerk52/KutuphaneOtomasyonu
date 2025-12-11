from flask import Blueprint, jsonify, request
from ..repositories.user_repo import (
    get_all_users, get_user_by_id, create_user, update_user, delete_user
)
from app.utils.jwt_maker import create_jwt
from ..repositories.user_repo import get_user_by_username
from app.utils.mail_sender import send_login_email
from ..repositories.user_repo import get_user_by_email

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True) or {}
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Geçersiz istek formatı (JSON bekleniyor)"
        }), 400

    email = data.get("email")
    password = data.get("password")

    # Boş alan kontrolü
    if not email or not password:
        return jsonify({
            "success": False,
            "message": "E-posta ve şifre gerekli"
        }), 400

    # Kullanıcıyı email ile bul
    user = get_user_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({
            "success": False,
            "message": "Geçersiz e-posta veya şifre"
        }), 401

    # JWT üret
    try:
        token = create_jwt(user.id, user.role)
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Sunucu hatası: Token oluşturulamadı"
        }), 500

    # Mail gönder (opsiyonel – hata verirse login bozulmasın)
    try:
        send_login_email(user.email, user.username)
    except Exception as e:
        print("MAIL GÖNDERME HATASI:", e)

    # Kullanıcının gideceği sayfayı belirle (admin: admin.html, user: index.html)
    redirect_url = "admin.html" if user.role == "admin" else "index.html"

    return jsonify({
        "success": True,
        "message": "Giriş başarılı",
        "token": token,
        "role": user.role,
        "username": user.username,
        "redirect_url": redirect_url
    }), 200


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify({
        "success": True,
        "count": len(users),
        "data": [user.to_dict() for user in users]
    })


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
    return jsonify(user.to_dict())


@user_bp.route('/users', methods=['POST'])
def register_user():
    try:
        data = request.get_json(force=True) or {}
    except Exception as e:
        return jsonify({'error': 'Eksik veya hatalı veri (Geçerli JSON bekleniyor)'}), 400

    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'Eksik veri'}), 400
    user = create_user(data['username'], data['email'], data['password'], data.get('role', 'user'))
    return jsonify(user.to_dict()), 201


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    try:
        data = request.get_json(force=True) or {}
    except Exception as e:
        return jsonify({'error': 'Eksik veya hatalı veri (Geçerli JSON bekleniyor)'}), 400

    user = update_user(user_id, data)
    if not user:
        return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
    return jsonify(user.to_dict())


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    ok = delete_user(user_id)
    if not ok:
        return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
    return jsonify({'result': True})