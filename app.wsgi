import sys
import logging
import os

#venv_activate = "/home/njz8626/venv/bin/activate"
#file_path = os.path.abspath(__file__)
#file_folder = os.path.join(file_path, "..")
#execfile(venv_activate, dict(__file__=venv_activate))

#sys.path.insert(0, file_folder)

from app import create_app, database_setup
from backend.db import Base
from configs import ProductionConfig

import site

from sqlalchemy import create_engine

# raise ValueError(sys.prefix + str(sys.path), site.USER_BASE, site.USER_SITE)

application = create_app(ProductionConfig)
#Base.metadata.create_all(
#    create_engine(application.config['SQLALCHEMY_DATABASE_URI'])
#)
