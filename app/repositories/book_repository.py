from app import db
from app.models import Book, Author, Category
# book_authors ilişkisel tablosunu N:M işlemleri için içe aktarıyoruz
from app.models.book import book_authors 

class BookRepository:
    
    @staticmethod
    def get_all_books():
        """Tüm kitapları, yazar ve kategori bilgileriyle çeker (JOIN)."""
        # db.joinedload ile ilişkili tabloları tek sorguda çekeriz (Eager Loading)
        return Book.query.options(db.joinedload(Book.authors), db.joinedload(Book.category)).all()

    @staticmethod
    def get_book_by_id(book_id):
        """ID'ye göre tek bir kitap çeker."""
        return Book.query.get(book_id)

    @staticmethod
    def get_books_by_ids(book_ids):
        """Bir ID listesine göre kitapları çeker."""
        return Book.query.filter(Book.id.in_(book_ids)).all()

    # --- CRUD İşlemleri (Admin tarafından kullanılır) ---
    
    @staticmethod
    def create_book(title, isbn, publication_year, stock, category_id, author_ids):
        """Yeni kitap ekler (CRUD - CREATE)."""
        
        # 1. Book nesnesi oluştur
        new_book = Book(
            title=title, 
            isbn=isbn, 
            publication_year=publication_year, 
            stock=stock, 
            category_id=category_id
        )
        
        # 2. Yazarları bul ve N:M ilişkiyi kur
        # Eğer yazar ID'leri yoksa (boş liste), kitap yazarsız kaydedilir
        if author_ids:
            authors = Author.query.filter(Author.id.in_(author_ids)).all()
            new_book.authors = authors # İlişki kurulur
            
        db.session.add(new_book)
        db.session.commit()
        return new_book

    @staticmethod
    def update_book(book_id, data):
        """Kitap bilgilerini günceller (CRUD - UPDATE)."""
        book = BookRepository.get_book_by_id(book_id)
        if not book:
            return None

        # Temel alanları güncelle
        book.title = data.get('title', book.title)
        book.isbn = data.get('isbn', book.isbn)
        book.publication_year = data.get('publication_year', book.publication_year)
        book.stock = data.get('stock', book.stock)
        book.category_id = data.get('category_id', book.category_id)
        
        # Yazarları güncelle (N:M ilişki)
        if 'author_ids' in data:
            new_author_ids = data['author_ids']
            new_authors = Author.query.filter(Author.id.in_(new_author_ids)).all()
            book.authors = new_authors # İlişkiyi yeniden kurar/günceller

        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id):
        """Kitap silme (CRUD - DELETE)."""
        book = BookRepository.get_book_by_id(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return True
        return False
        
    # --- Stok Yönetimi (Loan Service tarafından kullanılır) ---
    
    @staticmethod
    def update_stock(book_id, change):
        """Kitabın stok miktarını günceller (+1: iade, -1: ödünç)."""
        book = BookRepository.get_book_by_id(book_id)
        if book:
            # Stok değişimi yapılabilir mi kontrolü (Örn: stok 0'ın altına düşmemeli)
            if book.stock + change >= 0:
                book.stock += change
                db.session.commit()
                return book
            else:
                return None # Stok yetersiz
        return None
    
    # app/repositories/book_repository.py dosyasında, class BookRepository: bloğunun içine ekleyin:

    @staticmethod
    def save_book(book_obj):
        """Mevcut bir kitap objesinin (örneğin stoğunun) veritabanına kaydedilmesini sağlar."""
        from app import db # db objesini burada import etmeliyiz
        db.session.commit()
        return book_obj