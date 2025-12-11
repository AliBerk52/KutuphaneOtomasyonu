import jwt
from datetime import datetime, timedelta
from flask import current_app

def create_jwt(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    secret_key = current_app.config["SECRET_KEY"]
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    # jwt.encode returns a bytes object in PyJWT >=2.x, so decode if necessary
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token
