from app import db

class Penalty(db.Model):
    __tablename__ = 'penalty'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    
    # Yabancı Anahtar (1:1 ilişkiyi garanti etmek için unique)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), unique=True, nullable=False) 

    def __repr__(self):
        return f'<Penalty {self.amount}>'