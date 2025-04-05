import os
import dotenv
import json

dotenv.load_dotenv()

org_settings_path = os.environ.get("ORG_SETTINGS", "settings.json")

try:
    with open(org_settings_path) as f:
        data = json.load(f)
except FileNotFoundError:
    with open(org_settings_path, "w") as f:
        data = {
            "1": {
                "general_meetings_requirement": 16,
                "committee_meetings_requirement": 6,
                "social_meetings_requirement": 1,
                "volunteering_meetings_requirement": 1
            }
        }
        json.dump(data, f)

def update_org_settings(org: int, **kwargs):
    data.update({str(org): dict(**kwargs)})

    with open(org_settings_path, "w") as f:
        json.dump(data, f)

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    ORG_SETTINGS = data


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
    SERVER_NAME = "consortia.gccis.rit.edu"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"