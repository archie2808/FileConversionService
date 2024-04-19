
from .app_factory import create_app

app = create_app(config_filename='config.py')

if __name__ == "__main__":
    app.run()

#gunicorn -w 4 -b 0.0.0.0:5000 config:app
