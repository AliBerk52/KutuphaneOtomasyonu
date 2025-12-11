import os
import webbrowser
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Sadece ana process'te çalıştır
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open("http://127.0.0.1:5000")

    app.run(debug=True)
