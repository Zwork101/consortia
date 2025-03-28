from flask import Blueprint, jsonify, request, render_template

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

@test.route('/meetings/studentview', methods=['GET', 'POST'])
def studentview():
    return render_template('student-profile.html.j2')

@test.route("/notifications")
def return_notifications():
    return render_template("admin-notification-page.html.j2")

@test.route("/settingswic")
def return_settingswic():
    return render_template("configuration-wics.html.j2")

@test.route("/yearlyreports")
def return_yearlyreports():
    return render_template("yearly-reports.html.j2")

@test.route('/admin/update_attendance_data/<org>', methods=['POST'])
def update_attendance_data(org):
    if 'csv_data' not in request.files:  # Ensure file is uploaded
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    file = request.files['csv_data']  # Get file

    if not file or not file.filename:  # Ensure file has a name
        return jsonify({"success": False, "message": "No selected file"}), 400

    filename = file.filename  # Store filename
    if isinstance(filename, str) and filename.lower().endswith('.csv'):  # Check if it's a valid string
        file.save(f"./uploads/{filename}")  # Save file (update path as needed)
        return jsonify({"success": True, "file_name": filename})  # Success response

    return jsonify({"success": False, "message": "Invalid file type"}), 400