from app import db

class Author(db.Model):
    __tablename__ = 'author' # Bu ismin book_authors içindeki tanımla aynı olması şart
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Author {self.name}>'