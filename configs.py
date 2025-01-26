import os
import dotenv

dotenv.load_dotenv()

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    SERVER_NAME = "localhost"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class LocalConfig(Config):
    TESTING = True
    DEBUG = True
    SERVER_NAME = "localhost"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class ProductionConfig(Config):
    USE_X_SENDFILE = True