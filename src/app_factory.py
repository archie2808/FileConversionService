from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    
    # Register Blueprints
    from .routes import main as main_routes  # Ensure this import path is correct
    app.register_blueprint(main_routes)

    return app



SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'the_most_secret_of_keys')

