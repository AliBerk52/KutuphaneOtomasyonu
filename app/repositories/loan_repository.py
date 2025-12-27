from app import db
from sqlalchemy.orm import joinedload
# --- DÜZELTİLEN KISIM BAŞLANGICI ---
from app.models.loan import Loan       # Loan'ı kendi dosyasından al
from app.models.penalty import Penalty # Penalty'yi kendi dosyasından al (HATA BURADAYDI)
# --- DÜZELTİLEN KISIM BİTİŞİ ---

class LoanRepository:
    
    @staticmethod
    def get_loan_by_id(loan_id):
        """ID'ye göre ödünç işlemini getirir."""
        # İlişkileri çekerken hata olmaması için joinedload kullanıyoruz
        # NOT: Loan modelindeki ilişki adlarına göre burası 'user' ve 'book' olmalı
        return Loan.query.options(joinedload(Loan.user), joinedload(Loan.book)).get(loan_id)

    @staticmethod
    def get_active_loan_by_user_and_book(user_id, book_id):
        return Loan.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()

    @staticmethod
    def create_loan(loan_obj):
        db.session.add(loan_obj)
        db.session.commit()
        return loan_obj

    @staticmethod
    def save_loan(loan_obj):
        db.session.commit()
        return loan_obj

    @staticmethod
    def create_penalty(penalty_obj):
        db.session.add(penalty_obj)
        db.session.commit()
        return penalty_obj
        
    @staticmethod
    def get_active_loans_by_user(user_id):
        """Aktif ödünçleri listeler."""
        # Eager Loading: Kitap ve Kullanıcı verisini tek seferde çeker
        return db.session.execute(
            db.select(Loan)
            .options(
                joinedload(Loan.book), 
                joinedload(Loan.user)
            )
            .filter(
                Loan.user_id == user_id, 
                Loan.return_date == None 
            )
        ).scalars().all()
    

    @staticmethod
    def get_all_loans_with_details():
        """Admin için tüm ödünç alma işlemlerini kullanıcı ve kitap bilgileriyle getirir."""
        return Loan.query.all()