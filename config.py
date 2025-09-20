import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "preenroll.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False