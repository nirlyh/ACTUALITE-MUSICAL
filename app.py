# app.py

from app import create_app

# Je crée mon application Flask via la factory définie dans app/__init__.py
app = create_app()

if __name__ == "__main__":
    # Je lance mon application en mode debug pour le développement
    app.run(debug=True)
