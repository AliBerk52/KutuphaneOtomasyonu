from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
from app.models.loan import Loan
from app.models.user import User # Kullanıcı maili için gerekli
from datetime import datetime, timedelta
from flask_mail import Message
from app import mail, db

class LoanService:

    @staticmethod
    def get_active_loans_by_user(user_id):
        return LoanRepository.get_active_loans_by_user(user_id)

    @staticmethod
    def borrow_book(user_id, book_id):
        book = BookRepository.get_book_by_id(book_id)

        if not book:
            return {"message": "Kitap bulunamadı."}, 404
        
        if book.stock <= 0:
            return {"message": "Üzgünüz, stokta yeterli kitap yok."}, 400

        existing_loan = LoanRepository.get_active_loan_by_user_and_book(user_id, book_id)
        if existing_loan:
            return {"message": "Bu kitabı zaten ödünç almışsınız."}, 400

        try:
            loan_date = datetime.utcnow()
            due_date = loan_date + timedelta(days=14) 

            new_loan = Loan(
                user_id=user_id, 
                book_id=book_id,
                loan_date=loan_date,
                due_date=due_date
            )

            LoanRepository.create_loan(new_loan)
            book.stock -= 1
            BookRepository.save_book(book)

            # --- MAİL GÖNDERME BAŞLANGICI ---
            try:
                user = User.query.get(user_id)
                if user and user.email:
                    msg = Message(
                        subject="Kitap Ödünç Alma Onayı - Akıllı Kütüphane",
                        recipients=[user.email] # Config'deki mail adresine gider
                    )
                    msg.body = f"""
Sayın {user.username},

'{book.title}' isimli kitabı başarıyla ödünç aldınız.
İade etmeniz gereken son tarih: {due_date.strftime('%d.%m.%Y')}

Keyifli okumalar dileriz!
                    """
                    mail.send(msg)
                    print(f"Bilgilendirme maili gönderildi: {user.email}")
            except Exception as mail_err:
                print(f"Mail gönderilemedi (Ödünç alma başarılı): {mail_err}")
            # --- MAİL GÖNDERME BİTİŞİ ---

            return {"message": "Kitap başarıyla ödünç alındı. Bilgilendirme maili gönderildi.", "loan_id": new_loan.id}, 201
        
        except Exception as e:
            return {"message": f"Veritabanı hatası: {str(e)}"}, 500

  # app/services/loan_service.py içindeki return_book metodunu güncelleyelim

    @staticmethod
    def return_book(loan_id, user_id):
        loan = LoanRepository.get_loan_by_id(loan_id)

        if not loan or loan.user_id != user_id or loan.return_date is not None:
            return {"message": "Geçersiz işlem veya kitap zaten iade edilmiş."}, 400

        try:
            return_date = datetime.utcnow()
            loan.return_date = return_date
            loan.is_returned = True
            
            # --- CEZA HESAPLAMA MANTIĞI ---
            penalty_amount = 0
            # Eğer iade tarihi, teslim edilmesi gereken tarihi (due_date) geçmişse
            if return_date > loan.due_date:
                gecikme_suresi = (return_date - loan.due_date).days
                if gecikme_suresi > 0:
                    penalty_amount = gecikme_suresi * 50 # Günlük 50 TL
            
            # Stoğu artır
            book = BookRepository.get_book_by_id(loan.book_id)
            if book:
                book.stock += 1
                BookRepository.save_book(book)
            
            LoanRepository.save_loan(loan)

            # --- CEZA MAİLİ GÖNDERME ---
            user = User.query.get(user_id)
            if user and user.email:
                msg = Message(
                    subject="Kitap İade Onayı ve Ceza Bilgilendirmesi",
                    recipients=[user.email]
                )
                
                ceza_mesaji = f"Gecikme bedeli: {penalty_amount} TL." if penalty_amount > 0 else "Herhangi bir gecikme bedeli bulunmamaktadır."
                
                msg.body = f"""
Sayın {user.username},

'{book.title}' isimli kitabı iade ettiğiniz için teşekkür ederiz.

İade Detayları:
- Teslim Edilmesi Gereken Tarih: {loan.due_date.strftime('%d.%m.%Y')}
- İade Edilen Tarih: {return_date.strftime('%d.%m.%Y')}
- {ceza_mesaji}

İyi günler dileriz.
                """
                mail.send(msg)

            return {
                "message": "İade başarılı.", 
                "penalty": penalty_amount,
                "detail": f"{penalty_amount} TL ceza yansıtıldı." if penalty_amount > 0 else "Zamanında iade edildi."
            }, 200
        
        except Exception as e:
            return {"message": f"Hata: {str(e)}"}, 500