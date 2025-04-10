from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here to register them with SQLAlchemy
    from .models import Guest, Episode, Appearance

    # Register blueprint here to avoid circular import
    from .routes import bp
    app.register_blueprint(bp)

    return app
