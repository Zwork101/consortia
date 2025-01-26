from flask import Blueprint, render_template

admin = Blueprint("testing", __name__, static_folder="static/", template_folder="templates/")

@admin.route("/semester")
def return_semester():
    return render_template("current-semester-comms-interior.html")

@admin.route("/index")
def return_index():
    return render_template("index.html")

@admin.route("/profile")
def return_profile():
    return render_template("profile.html")