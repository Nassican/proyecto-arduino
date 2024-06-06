from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('server.config.Config')
    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    return app