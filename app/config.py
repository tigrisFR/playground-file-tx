import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "files.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3']) # Extend as necessary
    #JWT_CSRF_CHECK_FORM = False # Disabling CSRF for simplicity. Revisit in production.
    #JWT_CSRF_IN_COOKIES = False
    JWT_SECRET_KEY = process.env.JWT_SECRET_KEY
