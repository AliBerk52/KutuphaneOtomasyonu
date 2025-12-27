from app.repositories.author_repository import AuthorRepository
from app.repositories.category_repository import CategoryRepository

class AdminService:
    
    # --- Yazar İşlemleri ---
    @staticmethod
    def get_all_authors():
        authors = AuthorRepository.get_all_authors()
        return [{'id': a.id, 'name': a.name} for a in authors]

    @staticmethod
    def create_author(name):
        return AuthorRepository.create_author(name)

    @staticmethod
    def update_author(author_id, name):
        return AuthorRepository.update_author(author_id, name)
        
    @staticmethod
    def delete_author(author_id):
        # Silmeden önce yazara ait kitapların N:M ilişkisinin yönetilmesi gerekir
        return AuthorRepository.delete_author(author_id)


    # --- Kategori İşlemleri ---
    @staticmethod
    def get_all_categories():
        categories = CategoryRepository.get_all_categories()
        return [{'id': c.id, 'name': c.name} for c in categories]
        
    @staticmethod
    def create_category(name):
        return CategoryRepository.create_category(name)

    @staticmethod
    def update_category(category_id, name):
        return CategoryRepository.update_category(category_id, name)
        
    @staticmethod
    def delete_category(category_id):
        # Silmeden önce kategoriye bağlı kitaplar varsa silme işlemi engellenmeli/yönetilmeli
        return CategoryRepository.delete_category(category_id)