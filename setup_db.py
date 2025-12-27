from app import create_app, db
import os

# Uygulama bağlamını oluştur
app = create_app('development')

# Uygulama bağlamına gir
with app.app_context():
    # Mevcut veritabanındaki TÜM TABLOLARI siler (Dikkatli Kullanın!)
    # db.drop_all() 
    
    # Python modellerini kullanarak tabloları oluştur
    db.create_all()
    
    print("Veritabanı şeması (tablolar) başarıyla oluşturuldu!")

# NOT: Bu script'i her çalıştırdığınızda tabloyu yeniden oluşturmaya çalışır. 
# Eğer tablo zaten varsa hata vermez, ancak veri kaybını önlemek için 'drop_all()' kısmını kapalı tutun.