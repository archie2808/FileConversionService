
from .app_factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

#gunicorn -w 18 -b 0.0.0.0:5000 src.config:app
#nmon -f -s 3 -c 200 -F outputfilename.nmon

