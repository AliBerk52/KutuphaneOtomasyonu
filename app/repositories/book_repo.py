from app import db
from app.models.book import Book


def get_all_books():
    return Book.query.all()

def create_book(title, author, year):
    book = Book(title=title, author=author, year=year)
    db.session.add(book)
    db.session.commit()
    return book

def get_book_by_id(book_id):
    return Book.query.get(book_id)

def update_book(book_id, data):
    book = get_book_by_id(book_id)
    if not book:
        return None
    if 'title' in data and data['title']:
        book.title = data['title']
    if 'author' in data and data['author']:
        book.author = data['author']
    if 'year' in data:
        book.year = data['year']
    if 'status' in data:
        book.status = data['status']
    db.session.commit()
    return book

def delete_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return False
    db.session.delete(book)
    db.session.commit()
    return True