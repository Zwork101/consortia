import os

from dotenv import load_dotenv

load_dotenv()


from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]


class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = "localhost:8080"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class LocalConfig(Config):
    TESTING = True
    DEBUG = True
    SERVER_NAME = "ec2-54-196-105-29.compute-1.amazonaws.com:8080"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class ProductionConfig(Config):
    USE_X_SENDFILE = True