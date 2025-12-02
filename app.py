from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps
import jwt
import datetime
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Asdasd123!!'  # JWT secret

# -------------------------------
# MySQL Bağlantısı
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Asdasd123!!',      # kendi MySQL parolanı yaz
    database='kutuphane',      # senin DB adı
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

# -------------------------------
# JWT Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-tokens')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['id']
        except Exception:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

# -------------------------------
# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE fullname=%s AND password_=%s", (username, password))
    user = cursor.fetchone()
    if not user:
        return jsonify({'message': 'user or password wrong'}), 401

    token = jwt.encode({
        'id': user['id'],
        'is_admin': user['role'] == 'admin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

# -------------------------------
# GET /books
@app.route('/books', methods=['GET'])
@token_required
def get_books(current_user_id):
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return jsonify(books)

# -------------------------------
# POST /books (admin)
@app.route('/books', methods=['POST'])
@token_required
def add_book(current_user_id):
    cursor.execute("SELECT role FROM users WHERE id=%s", (current_user_id,))
    role = cursor.fetchone()['role']
    if role != 'admin':
        return jsonify({'message': 'unauthorized'}), 403

    data = request.get_json()
    cursor.execute(
        "INSERT INTO books (name, author_id, categories_id) VALUES (%s, %s, %s)",
        (data['name'], data['author_id'], data['categories_id'])
    )
    connection.commit()
    return jsonify({'message': 'Book add.'}), 201

# -------------------------------
# DELETE /books/<id> (admin)
@app.route('/books/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user_id, book_id):
    cursor.execute("SELECT role FROM users WHERE id=%s", (current_user_id,))
    role = cursor.fetchone()['role']
    if role != 'admin':
        return jsonify({'message': 'unauthorized'}), 403

    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    connection.commit()
    return jsonify({'message': 'Book deleted.'})

# -------------------------------
# PUT /books/<id> (admin)
@app.route('/books/<int:book_id>', methods=['PUT'])
@token_required
def update_book(current_user_id, book_id):
    cursor.execute("SELECT role FROM users WHERE id=%s", (current_user_id,))
    role = cursor.fetchone()['role']
    if role != 'admin':
        return jsonify({'message': 'unauthorized'}), 403

    data = request.get_json()
    cursor.execute("""
        UPDATE books 
        SET name=%s, author_id=%s, categories_id=%s 
        WHERE id=%s
    """, (data.get('name'), data.get('author_id'), data.get('categories_id'), book_id))
    connection.commit()
    return jsonify({'message': 'Book Updated.'})

# -------------------------------
# POST /borrow/<book_id>
@app.route('/borrow/<int:book_id>', methods=['POST'])
@token_required
def borrow_book(current_user_id, book_id):
    cursor.execute("SELECT available FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    if not book or not book['available']:
        return jsonify({'message': 'Kitap mevcut değil veya uygun değil'}), 400

    cursor.execute("""
        INSERT INTO borrow (user_id, book_id, borrow_date, due_date) 
        VALUES (%s, %s, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY))
    """, (current_user_id, book_id))

    cursor.execute("UPDATE books SET available = FALSE WHERE id = %s", (book_id,))
    connection.commit()
    return jsonify({'message': 'Kitap ödünç alındı.'})

# -------------------------------
# POST /return/<book_id>
@app.route('/return/<int:book_id>', methods=['POST'])
@token_required
def return_book(current_user_id, book_id):
    cursor.execute("""
        SELECT * FROM borrow 
        WHERE user_id=%s AND book_id=%s AND return_date IS NULL
    """, (current_user_id, book_id))
    record = cursor.fetchone()
    if not record:
        return jsonify({'message': 'Aktif ödünç kaydı yok'}), 404

    cursor.execute("UPDATE borrow SET return_date = NOW() WHERE id = %s", (record['id'],))
    cursor.execute("UPDATE books SET available = TRUE WHERE id = %s", (book_id,))
    connection.commit()
    return jsonify({'message': 'Kitap iade edildi. Ceza trigger ile hesaplanacak.'})

# -------------------------------
# GET /penalties (admin)
@app.route('/penalties', methods=['GET'])
@token_required
def get_penalties(current_user_id):
    cursor.execute("SELECT role FROM users WHERE id=%s", (current_user_id,))
    role = cursor.fetchone()['role']
    if role != 'admin':
        return jsonify({'message': 'Yetkisiz'}), 403

    cursor.execute("SELECT * FROM penalties")
    penalties = cursor.fetchall()
    return jsonify(penalties)

# -------------------------------
# Ana sayfa
@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

# Login sayfası
@app.route('/login-page', methods=['GET'])
def login_page():
    return render_template('login.html')

# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)

