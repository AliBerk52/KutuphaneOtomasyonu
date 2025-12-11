from app import db
from app.models.user import User

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_user(username, email, password, role="user"):
    user = User(
        username=username,
        email=email,
        role=role  
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user_id, data):
    user = get_user_by_id(user_id)
    if not user:
        return None
    if 'username' in data and data['username']:
        user.username = data['username']
    if 'email' in data and data['email']:
        user.email = data['email']
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    db.session.commit()
    return user

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True