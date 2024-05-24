from flask import Flask
from config import Config
from models import db
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os
from resources import api_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(api_bp, url_prefix='/api')

    # Set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/blogging_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Blogging App startup')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)