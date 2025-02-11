from flask import Blueprint

home = Blueprint("/", __name__, static_folder="static/", template_folder="templates/")

@home.route("/")
def homepage():
    return "Testing :)"