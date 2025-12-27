from flask import Blueprint, jsonify, request

from ..repositories.book_repo import (
    get_all_books, get_book_by_id, create_book, update_book, delete_book
)

book_bp = Blueprint('book', __name__)


@book_bp.route('/books', methods=['GET'])
def get_books():
    books = get_all_books()
    return jsonify({
        "success": True,
        "count": len(books),
        "data": [book.to_dict() for book in books]
    })


@book_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return jsonify({'error': 'Kitap bulunamadı'}), 404
    return jsonify(book.to_dict())


@book_bp.route('/books', methods=['POST'])
def add_book():
    data = request.json or {}
    if not all(k in data for k in ('title', 'author')):
        return jsonify({'error': 'Eksik veri'}), 400
    book = create_book(data.get('title'), data.get('author'), data.get('year'))
    return jsonify(book.to_dict()), 201


@book_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book_route(book_id):
    data = request.json or {}
    book = update_book(book_id, data)
    if not book:
        return jsonify({'error': 'Kitap bulunamadı'}), 404
    return jsonify(book.to_dict())


@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book_route(book_id):
    ok = delete_book(book_id)
    if not ok:
        return jsonify({'error': 'Kitap bulunamadı'}), 404
    return jsonify({'result': True})

from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository 
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.decorators import admin_required # Admin yetkisi kontrolü için içe aktarıldı

# Blueprint'i app/__init__.py dosyasında /api/v1/books prefix'i ile kaydettik.
book_bp = Blueprint('book_bp', __name__)

# --- 1. Halka Açık Rotalar (JWT Gerekmez) ---

@book_bp.route('/', methods=['GET'])
def list_books():
    """Tüm kitapları veya arama sonuçlarını listeler."""
    query = request.args.get('query') # Sorgu parametresi: /api/v1/books?query=python
    
    if query:
        # Arama mantığını Service katmanına devret
        books = BookService.search_books(query)
    else:
        # Tüm kitapları listele
        books = BookService.get_all_books()
        
    return jsonify({
        "success": True, 
        "count": len(books),
        "data": books
    }), 200

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Belirli bir kitabın detaylarını gösterir."""
    
    # Detay çekme mantığını Service katmanına devret
    result = BookService.get_book_details(book_id)
    
    if result.get("success"):
        return jsonify(result["book"]), 200
    else:
        return jsonify({"success": False, "message": "Kitap bulunamadı."}), 404

# --- 2. Admin CRUD Rotaları (JWT ve Admin Yetkisi Gerekir) ---

@book_bp.route('/', methods=['POST'])
@admin_required() 
def create_book():
    """Yeni kitap ekler."""
    data = request.get_json()
    
    # Gerekli alanlar kontrolü
    required_fields = ['title', 'isbn', 'stock', 'category_id', 'author_ids']
    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "message": "Eksik alanlar var. (title, isbn, stock, category_id, author_ids)"}), 400
        
    try:
        # Yeni kitabı Repository üzerinden ekle
        new_book = BookRepository.create_book(**data)
        return jsonify({
            "success": True, 
            "message": "Kitap başarıyla eklendi.",
            "book_id": new_book.id
        }), 201
    except Exception as e:
         return jsonify({"success": False, "message": f"Kitap eklenirken veritabanı hatası: {str(e)}"}), 500

@book_bp.route('/<int:book_id>', methods=['PUT', 'DELETE'])
@admin_required()
def book_detail_admin(book_id):
    if request.method == 'PUT':
        """Kitap bilgilerini günceller."""
        data = request.get_json()
        book = BookRepository.update_book(book_id, data)
        if book:
            return jsonify({"success": True, "message": "Kitap başarıyla güncellendi."}), 200
        return jsonify({"success": False, "message": "Kitap bulunamadı."}), 404

    elif request.method == 'DELETE':
        """Kitabı sistemden siler."""
        if BookRepository.delete_book(book_id):
            return jsonify({"success": True, "message": "Kitap başarıyla silindi."}), 204 # No Content
        return jsonify({"success": False, "message": "Kitap bulunamadı."}), 404

