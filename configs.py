import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]


class DevelopmentConfig(Config):
    TESTING = True,
    DEBUG = True
    SERVER_NAME = "ec2-3-88-17-77.compute-1.amazonaws.com:8080"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class ProductionConfig(Config):
    USE_X_SENDFILE = True