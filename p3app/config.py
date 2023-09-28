import os

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This should be the directory where `config.py` is.
    PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))  # This gets the parent directory of `BASE_DIR`.
    UPLOAD_FOLDER = os.path.join(PARENT_DIR, 'uploads')
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"PARENT_DIR: {PARENT_DIR}")
    print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "files.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3']) # Extend as necessary
    #JWT_CSRF_CHECK_FORM = False # Disabling CSRF for simplicity. Revisit in production.
    #JWT_CSRF_IN_COOKIES = False
    JWT_SECRET_KEY = 'pKu6p!NTHqXxvqa2Kf2mb!.RrHWjqJWp'
