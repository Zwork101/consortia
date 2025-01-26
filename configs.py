import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]


class DevelopmentConfig(Config):
    TESTING = True,
    DEBUG = True
    SERVER_NAME = "ec2-54-196-105-29.compute-1.amazonaws.com:8080"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class ProductionConfig(Config):
    USE_X_SENDFILE = True