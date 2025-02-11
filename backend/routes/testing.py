from flask import Blueprint, render_template

test = Blueprint("testing", __name__, static_folder="static/", template_folder="templates/")


@test.route("/index")
def return_index():
    return render_template("index.html.j2")

@test.route("/profile")
def return_profile():
    return render_template("profile.html")

@test.route("/comms-int")
def return_comms_int():
    return render_template("current-semester-comms-interior.html.j2")

@test.route("/wic-int")
def return_wic_int():
    return render_template("current-semester-wic-history-interior.html.j2")

@test.route("/semester")
def return_semester():
    return render_template("current-semester-wics.html.j2")

@test.route("/db-comms")
def return_db_coms():
    return render_template("database-view-coms.html.j2")

@test.route("/db-wic")
def return_db_wic():
    return render_template("database-view-wic.html.j2")
