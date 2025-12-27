from flask import Blueprint, jsonify, request
from app.services.admin_service import AdminService
from flask_jwt_extended import jwt_required, get_jwt
from app.decorators import admin_required # Admin yetkisi kontrolü için içe aktarıldı
from flask import render_template 



# Blueprint'i app/__init__.py dosyasında /api/v1/admin prefix'i ile kaydettik.
admin_bp = Blueprint('admin_bp', __name__)



@admin_bp.route('/admin-panel', methods=['GET'])
@admin_required()
def admin_panel_view():
    """Admin Panel HTML sayfasını yükler."""
    return render_template('admin_panel.html')




@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required()
def categories():
    """Tüm kategorileri listeler (GET) veya yeni kategori ekler (POST)."""
    if request.method == 'GET':
        data = AdminService.get_all_categories()
        return jsonify({"success": True, "data": data}), 200
        
    elif request.method == 'POST':
        name = request.get_json().get('name')
        if not name:
            return jsonify({"success": False, "message": "Kategori adı gerekli."}), 400
        
        try:
            new_category = AdminService.create_category(name)
            return jsonify({"success": True, "message": "Kategori başarıyla eklendi.", "id": new_category.id}), 201
        except Exception as e:
            # Örneğin, unique kısıtlaması hatası
            return jsonify({"success": False, "message": f"Kategori eklenirken hata: {str(e)}"}), 409

@admin_bp.route('/categories/<int:category_id>', methods=['PUT', 'DELETE'])
@admin_required()
def category_detail(category_id):
    """Belirli bir kategoriyi günceller (PUT) veya siler (DELETE)."""
    if request.method == 'PUT':
        name = request.get_json().get('name')
        if not name:
            return jsonify({"success": False, "message": "Kategori adı gerekli."}), 400
        
        category = AdminService.update_category(category_id, name)
        if category:
            return jsonify({"success": True, "message": "Kategori başarıyla güncellendi."}), 200
        return jsonify({"success": False, "message": "Kategori bulunamadı."}), 404

    elif request.method == 'DELETE':
        # ÖNEMLİ: Gerçek sistemde, ilişkisel veri bütünlüğü (Foreign Key) kontrol edilmelidir.
        if AdminService.delete_category(category_id):
            return jsonify({"success": True, "message": "Kategori başarıyla silindi."}), 204 # No Content
        return jsonify({"success": False, "message": "Kategori bulunamadı."}), 404

# --- 2. YAZAR (AUTHOR) CRUD İŞLEMLERİ (Admin Gerekir) ---

@admin_bp.route('/authors', methods=['GET', 'POST'])
@admin_required()
def authors():
    """Tüm yazarları listeler (GET) veya yeni yazar ekler (POST)."""
    if request.method == 'GET':
        data = AdminService.get_all_authors()
        return jsonify({"success": True, "data": data}), 200
        
    elif request.method == 'POST':
        name = request.get_json().get('name')
        if not name:
            return jsonify({"success": False, "message": "Yazar adı gerekli."}), 400
        
        try:
            new_author = AdminService.create_author(name)
            return jsonify({"success": True, "message": "Yazar başarıyla eklendi.", "id": new_author.id}), 201
        except Exception as e:
            return jsonify({"success": False, "message": f"Yazar eklenirken hata: {str(e)}"}), 409


@admin_bp.route('/authors/<int:author_id>', methods=['PUT', 'DELETE'])
@admin_required()
def author_detail(author_id):
    """Belirli bir yazarı günceller (PUT) veya siler (DELETE)."""
    if request.method == 'PUT':
        name = request.get_json().get('name')
        if not name:
            return jsonify({"success": False, "message": "Yazar adı gerekli."}), 400
        
        author = AdminService.update_author(author_id, name)
        if author:
            return jsonify({"success": True, "message": "Yazar başarıyla güncellendi."}), 200
        return jsonify({"success": False, "message": "Yazar bulunamadı."}), 404

    elif request.method == 'DELETE':
        # ÖNEMLİ: Yazar silinmeden önce N:M ilişki tablosu (book_authors) güncellenmelidir.
        if AdminService.delete_author(author_id):
            return jsonify({"success": True, "message": "Yazar başarıyla silindi."}), 204
        return jsonify({"success": False, "message": "Yazar bulunamadı."}), 404