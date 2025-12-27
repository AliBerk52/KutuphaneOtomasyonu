from app import db

# Yazarlar için ara tablo (Önceki hatada düzeltmiştik)
book_authors = db.Table('book_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    publication_year = db.Column(db.Integer)
    stock = db.Column(db.Integer, default=0)
    
    # Kategori bağlantısı
    category_id = db.Column(db.Integer, db.ForeignKey('category.id')) # 'category.id' yazdığından emin ol

    # İlişkiler
    authors = db.relationship('Author', secondary=book_authors, backref=db.backref('books', lazy='dynamic'))
    category = db.relationship('Category', backref=db.backref('books', lazy='dynamic'))