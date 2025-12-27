from app.repositories.book_repository import BookRepository

class BookService:
    
    @staticmethod
    def get_all_books():
        """Tüm kitapları yazar ve kategori bilgileriyle birlikte çeker."""
        books = BookRepository.get_all_books()
        return BookService._serialize_books(books)

    @staticmethod
    def get_book_details(book_id):
        """Belirli bir kitabın detaylarını getirir."""
        book = BookRepository.get_book_by_id(book_id)
        if book:
            return {"success": True, "book": BookService._serialize_book(book)}
        return {"success": False, "message": "Kitap bulunamadı."}, 404

    @staticmethod
    def search_books(query):
        """Başlık, yazar veya ISBN'e göre kitap arar. (Basit filtreleme mantığı)"""
        # Gerçek bir arama için Repository'ye yeni bir metod eklememiz gerekir.
        # Şimdilik tüm kitaplar üzerinde Python ile filtreleme yapalım:
        all_books = BookRepository.get_all_books()
        
        results = [
            book for book in all_books 
            if query.lower() in book.title.lower() 
            or any(query.lower() in author.name.lower() for author in book.authors)
            or query == book.isbn
        ]
        
        return BookService._serialize_books(results)

    # --- Yardımcı Metotlar (JSON serileştirme) ---
    @staticmethod
    def _serialize_book(book):
        """Tek bir Book model nesnesini API çıktısı için dict/JSON formatına dönüştürür."""
        return {
            'id': book.id,
            'title': book.title,
            'isbn': book.isbn,
            'publication_year': book.publication_year,
            'stock': book.stock,
            'category': book.category.name,
            'category_id': book.category_id,
            'authors': [author.name for author in book.authors]
        }

    @staticmethod
    def _serialize_books(books):
        """Kitap listesini serileştirir."""
        return [BookService._serialize_book(book) for book in books]