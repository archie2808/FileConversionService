from flask import Flask
import os


def create_app(config_filename=None , testing=True):

    app = Flask(__name__)

    if config_filename:
        app.config.from_pyfile(config_filename)

    # Register Blueprints
    from .routes import main as main_routes
    app.register_blueprint(main_routes)


    return app
#

SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'the_most_secret_of_keys')

