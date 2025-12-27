# app/models/__init__.py

from .user import User
from .author import Author
from .category import Category
from .book import Book, book_authors 
from .loan import Loan
from .penalty import Penalty

# Diğer katmanlarda sadece 'from app.models import User, Book' demek yeterli olacaktır.