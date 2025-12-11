from flask_mail import Message
from app import mail

def send_login_email(to_email, username):
    msg = Message(
        subject="Giriş Başarılı",
        recipients=[to_email],
        body=f"Merhaba {username}, sisteme başarıyla giriş yaptınız."
    )
    mail.send(msg)
