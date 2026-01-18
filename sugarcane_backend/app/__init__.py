from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

db = SQLAlchemy()
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Database configuration
    database_path = os.path.join(os.path.dirname(__file__), '..', 'predictions.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    logger.info(f"📁 Database path: {database_path}")
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS - CRITICAL for frontend to connect
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "http://localhost:5173",  # Vite default
                "http://127.0.0.1:3000",
                "http://127.0.0.1:5173"
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True
        }
    })
    
    logger.info("✅ CORS enabled for frontend communication")
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        try:
            db.create_all()
            logger.info("✅ Database tables created")
        except Exception as e:
            logger.error(f"❌ Database error: {str(e)}")
    
    return app
