from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('login.html')

@main_bp.route('/login')
def login_page():
    return render_template('login.html')

# --- YENİ EKLENEN ROTA ---
@main_bp.route('/register')
def register_page():
    """Kullanıcı kayıt sayfası."""
    return render_template('register.html')
# -------------------------

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/admin-panel')
def admin_panel():
    return render_template('admin_panel.html')