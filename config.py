import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session security and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database location - SQLite file stored in the app folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app', 'users.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False