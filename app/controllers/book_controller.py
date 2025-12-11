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