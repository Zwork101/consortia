from backend.email import get_token, send_email

from flask import Blueprint, render_template, redirect, url_for

test = Blueprint("testing", __name__, static_folder="static/", template_folder="templates/")


@test.route("/index")
def return_index():
    return render_template("index.html.j2")


@test.route("/comms-int")
def return_comms_int():
    return render_template("current-semester-comms-interior.html.j2")

@test.route("/wic-int")
def return_wic_int():
    return render_template("current-semester-wic-history-interior.html.j2")

@test.route("/coms-int")
def return_coms_hist():
    return render_template("current-semester-coms-history-interior.html.j2")

@test.route("/semester")
def return_semester():
    return render_template("current-semester-wics.html.j2")

@test.route("/db-comms")
def return_db_coms():
    return render_template("database-view-coms.html.j2")

@test.route("/db-wic")
def return_db_wic():
    return render_template("database-view-wic.html.j2")

@test.route("/wic")
def return_wic():
    return render_template("wics-profile.html.j2")

@test.route("/coms")
def return_coms():
    return render_template("coms-profile.html.j2")


@test.route("/com-email")
def return_com_email():
    return render_template("comsemail.html.j2", member_name="John Doe", points="5", events=[{
        "title": "Meeting 1",
        "date": "2021-03-01",
        "event": "Meeting",
        "location": "Zoom",
        "time": "5:00 PM",
        "link": "https://www.google.com",
        "points": 1,
        "description": "Meeting to discuss upcoming events"
    }, {
        "title": "Meeting 2",
        "date": "2021-03-01",
        "event": "Meeting",
        "location": "GOL 123",
        "time": "5:00 PM",
        "link": "https://www.google.com",
        "points": 4,
        "description": "Meeting to discuss upcoming events"
    }, {
        "title": "Meeting 3",
        "date": "2021-03-01",
        "event": "Meeting",
        "location": "Zoom",
        "time": "5:00 PM",
        "link": "https://www.google.com",
        "points": 3,
        "description": "Meeting to discuss upcoming events"
    }])

@test.route("/wic-email")
def return_wic_email():
    return render_template("wicemail.html.j2", member_name="John Doe", points="1", events=[{
        "title": "Meeting",
        "date": "2021-03-01",
        "event": "Meeting",
        "location": "Zoom",
        "time": "5:00 PM",
        "link": "https://www.google.com",
        "points": 1,
        "description": "Meeting to discuss upcoming events"
    }, {
        "title": "Meeting",
        "date": "2021-03-01",
        "event": "Meeting",
        "location": "Zoom",
        "time": "5:00 PM",
        "link": "https://www.google.com",
        "points": 1,
        "description": "Meeting to discuss upcoming events"
    }, {
        "title": "Meeting",
        "date": "2021-03-01",
        "event": "Meeting",
        "location": "Zoom",
        "time": "5:00 PM",
        "link": "https://www.google.com",
        "points": 1,
        "description": "Meeting to discuss upcoming events"
    }])

@test.route("/award-email")
def return_award_email():
    return render_template("awardemail.html.j2", member_name="John Doe", points="1", award=" A Sweat Shirt", semesters = 2, signature="Wic Admin")

@test.route("/calendar")
def return_calendar():
    return render_template("calendar.html.j2")

@test.route('/meetings/upload', methods=['GET', 'POST'])
def upload_meeting_data():
    return render_template('database-view-wic.html.j2')

@test.route('/meetings/attendance', methods=['GET', 'POST'])
def attendance_data():
    return render_template('database-view-attendance.html.j2')

@test.route('/meetings/student', methods=['GET', 'POST'])
def student_view_data():
    return render_template('database-view-student.html.j2')

@test.route("/testemail/<int:org>")
def test_email(org: int):
    cred = get_token(org)
    if cred is None:
        return redirect(
            url_for("oauth.authorize_email", org=org)
        )
    else:
        send_email(
            "<h1>Hello</h1><br><p>World</p>",
            "Email Test!",
            cred[1],
            ["njz8626@g.rit.edu", "rl2939@rit.edu"],
            cred[0]
        )
        return "Sent!"