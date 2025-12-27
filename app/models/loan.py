from app import db
from datetime import datetime

class Loan(db.Model):
    __tablename__ = 'loan'
    
    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False) 
    return_date = db.Column(db.DateTime, nullable=True) 
    is_returned = db.Column(db.Boolean, default=False)

    # Yabancı Anahtarlar (FOREIGN KEYS)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    # İlişkiler: İlişki adını sade (user, book) tuttuk. backref'ler diğer dosyalarda tanımlı.
   # User ile ilişki: borrower_rel adıyla User üzerinden erişilebilir hale getiriyoruz
    user = db.relationship('User', backref=db.backref('loan_records', lazy='dynamic'))
    
    # Book ile ilişki
    book = db.relationship('Book', backref=db.backref('loan_entries', lazy='dynamic'))

    # 3. Ceza (Penalty) İlişkisi:
    penalty = db.relationship('Penalty', backref='loan_info', uselist=False)

    def __repr__(self):
        return f'<Loan {self.id} by User {self.user_id}>'