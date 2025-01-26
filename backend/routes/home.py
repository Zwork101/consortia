from flask import Blueprint

home = Blueprint("home", __name__, static_folder="static/", template_folder="templates/")

@home.route("/")
def homepage():
    return "Testing :)"