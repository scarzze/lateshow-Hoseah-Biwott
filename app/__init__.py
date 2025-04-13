from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here to ensure they are registered with SQLAlchemy
    from .models import Guest, Episode, Appearance

    # Register blueprint to handle routes
    from .routes import bp
    app.register_blueprint(bp)

    return app
