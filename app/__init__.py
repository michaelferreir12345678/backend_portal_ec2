from flask import Flask
from flask_cors import CORS
from app.extensions import db, login_manager, migrate
from app.config import Config
from app.routes.errors import errors_bp
from app.routes.inconsistencies import inconsistencies_bp
from app.routes.process import process_bp
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    CORS(app) 
    app.config.from_object(Config)
    
    app.register_blueprint(errors_bp)
    app.register_blueprint(inconsistencies_bp)
    app.register_blueprint(process_bp)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    app.register_blueprint(auth_bp)

    return app
