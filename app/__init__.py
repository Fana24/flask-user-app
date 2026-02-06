from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config

# Initialize extensions without binding to app yet
db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Bind extensions to the app
    db.init_app(app)
    csrf.init_app(app)
    
    # Register the routes blueprint
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app