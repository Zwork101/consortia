import importlib
import os
import logging

from backend.db import db, db_testing_setup, Event
from configs import *

from flask import Flask, Blueprint

def create_app(config_file: Config = DevelopmentConfig) -> Flask:

    logging.basicConfig(level=logging.INFO)
    
    app = Flask(__name__, static_folder="static/", template_folder="templates/")

    app.config.from_object(config_file)

    db.init_app(app)

    blueprint_paths = os.listdir("backend/routes")
    blueprints = []

    for blueprint_path in blueprint_paths:

        if blueprint_path.startswith("__") or blueprint_path.startswith("."):
            continue

        module = importlib.import_module(f"backend.routes.{blueprint_path[:-3]}")
        for _, value in module.__dict__.items():
            if isinstance(value, Blueprint):
                blueprints.append(value)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        logging.info(f"Added '{blueprint.name}' blueprint.")

    return app

def database_setup(app):
    with app.app_context():
        db.create_all()
        
        if Event.query.get(8080) is None:
            db_testing_setup()
        
        db.session.commit()

if __name__ == "__main__":
    app = create_app(DevelopmentConfig)
    database_setup(app)
    app.run()
