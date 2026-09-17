from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.database import db
from app.routes.task_routes import task_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    app.register_blueprint(task_bp)

    with app.app_context():
        db.create_all()

    return app