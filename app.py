import importlib
import os
import logging

from backend.auth import shib
from backend.db import Administrator, Organizations, Organizer, Profile, RoleType, commit, db, db_testing_setup, Event, make_admin
from configs import *

from flask import Flask, Blueprint, request

def create_app(config_file: Config = DevelopmentConfig) -> Flask:

    logging.basicConfig(level=logging.INFO, filename="development.log", filemode="a")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
    
    app = Flask(__name__, static_folder="static/", template_folder="templates/")

    app.config.from_object(config_file)

    db.init_app(app)
    shib.init_app(app)

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

    app.jinja_env.add_extension("jinja2.ext.loopcontrols")

    with app.app_context():
        db.create_all()

        defacto_admin = db.session.query(Administrator.id).join(Profile).where(Profile.rit_id == app.config['DEFACTO_ADMIN']['rit_id']).first()
        if defacto_admin is None:
            WiC = Organizer(
                name = "Women in Computing",
                email = "wic@rit.edu"
            )
            
            COMS = Organizer(
                name = "Computing Organization for Multicultural Students",
                email = "coms@rit.edu"
            )

            profile = db.session.query(Profile.rit_id).where(Profile.rit_id == app.config['DEFACTO_ADMIN']['rit_id']).first()
            if profile is None:
                profile = Profile(**app.config['DEFACTO_ADMIN'])
            commit(profile, WiC, COMS)
            make_admin(profile.profile_id, Organizations.COMS, RoleType.ADMIN)
            make_admin(profile.profile_id, Organizations.WIC, RoleType.ADMIN)
            commit()

    return app

def database_setup(app):
    with app.app_context():
        db.create_all()
        
        if Event.query.first() is None:
            db_testing_setup()
        
        db.session.commit()

if __name__ == "__main__":
    app = create_app(DevelopmentConfig)

    ### REMOVE FROM PRODUCTION ###
    @app.before_request
    def before_request():
        request.environ["uid"] = "wls1234"
        request.environ["givenName"] = "Will"
        request.environ["sn"] = "Smith"
        request.environ["email"] = "wls1234@rit.edu"

    database_setup(app)
    app.run()
