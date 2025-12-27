
import os
import webbrowser
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Sadece ana process'te çalıştır
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open("http://127.0.0.1:5000")

    app.run(debug=True)

from app import create_app
import os

# Konfigürasyon adını ortam değişkeninden veya varsayılan olarak 'development' olarak al
config_name = os.environ.get('FLASK_CONFIG', 'development') 

# Uygulamayı başlat
app = create_app(config_name)

if __name__ == '__main__':
    # Flask uygulamasını varsayılan portta ve debug modunda başlatır
    app.run(debug=True)

    

