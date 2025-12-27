from app import db
from app.models import Author

class AuthorRepository:
    
    @staticmethod
    def get_all_authors():
        return Author.query.all()

    @staticmethod
    def get_author_by_id(author_id):
        return Author.query.get(author_id)

    @staticmethod
    def create_author(name):
        new_author = Author(name=name)
        db.session.add(new_author)
        db.session.commit()
        return new_author

    @staticmethod
    def update_author(author_id, name):
        author = AuthorRepository.get_author_by_id(author_id)
        if author:
            author.name = name
            db.session.commit()
            return author
        return None

    @staticmethod
    def delete_author(author_id):
        author = AuthorRepository.get_author_by_id(author_id)
        if author:
            db.session.delete(author)
            db.session.commit()
            return True
        return False