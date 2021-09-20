from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)


    db.init_app(app)

    from .Menu import main
    app.register_blueprint(main)

    return app