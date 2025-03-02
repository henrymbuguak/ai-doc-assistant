import os
from flask import Flask
from .routes import main_bp

def create_app():
    app = Flask(__name__)
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.py')
    app.config.from_pyfile(config_path)

    app.register_blueprint(main_bp)

    return app
