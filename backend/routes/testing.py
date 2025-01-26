from flask import Blueprint, render_template

admin = Blueprint("testing", __name__, static_folder="static/", template_folder="templates/")

@admin.route("/semester")
def return_semester():
    return render_template("current-semester-comms-interior.html")