from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def admin_required():
    """JWT payload'dan rol bilgisini çekerek Admin yetkisini kontrol eden dekoratör."""
    def wrapper(fn):
        # Bu iç fonksiyon, Blueprint'e bir view fonksiyonu olarak kaydedilecektir.
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user_claims = get_jwt()
            # JWT payload içindeki role bilgisini kontrol et
            if current_user_claims.get('role') != 'admin':
                return jsonify(msg="Bu işlem için yönetici yetkisi gereklidir."), 403
            return fn(*args, **kwargs)
        
        # Flask, decorator adını kullandığı için, aynı dekoratörü kullanan her rota 
        # aynı view fonksiyonu adını (decorator) kaydetmeye çalışıyordu.
        # Bu sorunu çözmek için, Flask'e benzersiz bir uç nokta (endpoint) adı vermesini sağlamalıyız.
        
        # Orijinal fonksiyon adını (fn.__name__) kullanarak benzersiz bir ad oluşturulur
        decorator.__name__ = fn.__name__ 
        
        return decorator
    return wrapper

# Diğer yetkilendirme veya yardımcı dekoratörler buraya eklenebilir.