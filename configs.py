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
            },
            "2": {
                "attendance": [
                    {"percent": 100, "points": 3},
                    {"percent": 75, "points": 2},
                    {"percent": 50, "points": 1}
                ],
                "volunteer": [
                    {"threshold": 9, "points": 4},
                    {"threshold": 6, "points": 3},
                    {"threshold": 3, "points": 2},
                    {"threshold": 1, "points": 1},
                ],
                "mentorship_minimum": 3,
                "mentorship_maximum": 9,
                "required_points": 18
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
    DEFACTO_ADMIN = {
        "rit_id": "njz8626",
        "first_name": "Nathan",
        "last_name": "Zilora",
        "email": "njz8626@rit.edu"
    }


class LocalConfig(Config):
    TESTING = True
    DEBUG = True
    SERVER_NAME = "ec2-54-196-105-29.compute-1.amazonaws.com:8080"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class ProductionConfig(Config):
    USE_X_SENDFILE = True
    SERVER_NAME = "consortia.gccis.rit.edu"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    #SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://consortia:{os.environ['DB_PASSWORD']}@localhost:3306/consortia"
    DEFACTO_ADMIN = {
        "rit_id": "njz8626",
        "first_name": "Nathan",
        "last_name": "Zilora",
        "email": "njz8626@rit.edu"
    }
