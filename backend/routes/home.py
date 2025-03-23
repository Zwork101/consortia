from flask import Blueprint, render_template

home = Blueprint("/", __name__, static_folder="static/", template_folder="templates/")

@home.route("/")
def homepage():
    return render_template("index.html.j2", title="Homepage")