from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.loan_service import LoanService
from app.repositories.loan_repository import LoanRepository


loan_bp = Blueprint('loan', __name__, url_prefix='/api/v1/loans')

@loan_bp.route('/my-loans', methods=['GET']) 
@jwt_required()
def list_user_active_loans():
    try:
        # User ID'yi sayıya çeviriyoruz (ÖNEMLİ)
        current_user_id = int(get_jwt_identity()) 
        
        active_loans = LoanService.get_active_loans_by_user(current_user_id) 
        
        data = [{
            'loan_id': loan.id, 
            'book_id': loan.book_id,
            # Loan modelindeki ilişki adları 'book' ve 'user' varsayılmıştır
            'book_title': loan.book.title if loan.book else 'Bilinmiyor',
            'issue_date': loan.loan_date.strftime('%Y-%m-%d'), 
            'due_date': loan.due_date.strftime('%Y-%m-%d'),     
            'is_returned': loan.return_date is not None,
            'return_date': loan.return_date.strftime('%Y-%m-%d') if loan.return_date else None,
        } for loan in active_loans] 
        
        return jsonify({
            "success": True,
            "count": len(data),
            "data": data
        }), 200

    except Exception as e:
        print(f"Listeleme Hatası: {e}")
        return jsonify({"success": False, "message": "Listeleme hatası oluştu."}), 500

@loan_bp.route('/borrow', methods=['POST'])
@jwt_required() 
def borrow_book():
    try:
        # User ID'yi sayıya çeviriyoruz (ÖNEMLİ)
        user_id = int(get_jwt_identity()) 
        
        data = request.get_json()
        book_id = data.get('book_id')
        
        if not book_id:
            return jsonify({"message": "Kitap ID'si gerekli."}), 400

        result, status_code = LoanService.borrow_book(user_id, book_id)
        return jsonify(result), status_code

    except Exception as e:
        print(f"Ödünç Alma Hatası: {e}")
        return jsonify({"message": "İşlem başarısız."}), 500
    

    # app/controllers/loan_controller.py dosyasında, en alta ekleyin:

# --- İADE İŞLEMİ ROTASI (POST) ---
@loan_bp.route('/return/<int:loan_id>', methods=['POST'])
@jwt_required()
def return_book(loan_id):
    try:
        # JWT'den gelen string user_id'yi int'e çeviriyoruz
        user_id = int(get_jwt_identity())
        
        # Service katmanına yönlendir
        result, status_code = LoanService.return_book(loan_id, user_id)
        
        return jsonify(result), status_code
    
    except Exception as e:
        print(f"İade İşlemi Hatası: {e}")
        # Frontend'e 500 hatası döndür, böylece JS hata mesajını gösterebilir.
        return jsonify({"message": "İade işlemi sırasında sunucu hatası oluştu."}), 500
    



@loan_bp.route('/admin/all-loans', methods=['GET'])
@jwt_required()
def get_all_loans_for_admin():
    """Tüm kullanıcıların ödünç işlemlerini admin paneli için listeler."""
    # Burada normalde admin kontrolü (identity['role'] == 'admin') yapılmalıdır
    loans = LoanRepository.get_all_loans_with_details()
    
    result = []
    for loan in loans:
        result.append({
            'id': loan.id,
            'user_email': loan.borrower_rel.email, # Kullanıcı bilgisi
            'book_title': loan.book.title,         # Kitap bilgisi
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'return_date': loan.return_date.strftime('%Y-%m-%d') if loan.return_date else None,
            'status': 'İade Edildi' if loan.return_date else 'Ödünçte'
        })
    return jsonify(result), 200