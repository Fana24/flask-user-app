import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key - use environment variable in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # Use DATABASE_URL from environment (Render provides this)
    # Fall back to SQLite for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app', 'users.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False