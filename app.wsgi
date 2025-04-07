import sys
import logging
import os

from app import create_app, database_setup
from backend.db import Base
from configs import ProductionConfig

file_path = os.path.abspath(__file__)
file_folder = os.path.join(file_path, "..")

application = create_app(ProductionConfig)
Base.metadata.create_all()
