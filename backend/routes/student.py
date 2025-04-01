from datetime import date

from backend.db import Event, Profile, db

from flask_login import current_user
from flask import Blueprint, abort, jsonify, request, render_template
from flask_wtf import FlaskForm

from sqlalchemy import case, desc
from wtforms import Form

student = Blueprint("student", __name__, static_folder="static/", template_folder="templates/")

@student.route("/wic")
def wic_homepage():
    return render_template("wics-profile.html.j2", title="WIC")

@student.route("/coms")
def coms_homepage():
    return render_template("coms-profile.html.j2", title="COMS")

@student.route("/profile", methods=["GET"])
def return_profile():
    org = request.args.get("org", type=int)
    if org:
        return current_user.serialize(org)
    else:
        return current_user.serialize()
    return abort(403)

@student.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('student-profile.html.j2')

@student.route("/meetings/<int:org>")
def upcoming_meetings(org: int):
    """Return upcoming meetings based on pagination parameters."""
    try:
        skip = request.args.get("skip", 0, type=int)
        count = request.args.get("count", 9999, type=int)

        if skip < 0 or count <= 0:
            return jsonify({"Error": "Invalid pagination parameters"})
    except ValueError:
        return jsonify({"Error": "Invalid input type"})

    meeting_results = (
        Event.query.filter(Event.organizer_id == org)
        .order_by(Event.start_time)
        .offset(skip)
        .all()
    )

    meetings = [
        {
            "event_id": meeting.event_id,
            "meeting_type": meeting.meeting_type.value,
            "name": meeting.name,
            "start_time": meeting.start_time.isoformat(),
            "end_time": meeting.end_time.isoformat(),
            "description": meeting.description,
            "point_value": meeting.point_value,
            "organizer_id": meeting.organizer_id,
            "semester": meeting.semester,
            "organizer": {
                 "profile_id": meeting.organizer.organization_id,  # updated field name
                 "name": meeting.organizer.name,
                 "email": meeting.organizer.email
             } if meeting.organizer else None,
             "attendants": [
                 {
                     "profile_id": attendee.profile_id,
                     "rit_id": attendee.rit_id,
                     "last_name": attendee.last_name,
                     "first_name": attendee.first_name,
                     "email": attendee.email
                 }
                 for attendee in meeting.attendants
             ]
        }
        for meeting in meeting_results
    ]
    return jsonify({"Meetings": meetings})

@student.route("/attendance")
def member_attendance():
    profile_id = 5 # request.get_json()
    # if not profile_id not in profile_id:
    #     return jsonify({"error": "Missing profile_id in request"})

    # id = profile_id.get("profile_id")  # ????
    attendance = Profile.query.filter(Profile.profile_id == profile_id).all()
    user_attendance = [
        {
            "profile_id": attendee.profile_id,
            "rit_id": attendee.rit_id,
            "last_name": attendee.last_name,
            "first_name": attendee.first_name,
            "attendance": attendee.attendance
        }
        for attendee in attendance
    ]
    return jsonify(user_attendance)


@student.route("/profile/attendance/<int:meeting_id>")
def get_attendance(meeting_id: int):

    meeting = Event.query.get(Event.event_id)

    if meeting is None:
        return abort(404)
    
    record = Profile.query.filter(meeting==meeting_id, Profile.profile_id==current_user.rit_id).all()
    
    if record is None:
        return abort(404)
    
    return jsonify(
        record.serialize(meeting_id)
    )

@student.route('/?sort=semester')
def sort_semester():
    semesters = Event.query.order_by(Event.semester).all()

    semester_wics = [
        {
            "semester_wics": "Spring" if sem.semester % 10 == 0 else "Fall",
            "year_wics": str(sem.semester // 10),
            "organizer_wics": sem.organizer == "wics",
            "meeting_type_wics": sem.meeting_type,
            "description_wics": sem.description,
            "point_value_wics": sem.point_value
        }
        for sem in semesters
    ]

    semester_coms = [
        {
            "semester_coms": "Spring" if sem.semester % 10 == 0 else "Fall",
            "year_coms": str(sem.semester // 10),
            "organizer_coms": sem.organizer == "coms",
            "meeting_type_coms": sem.meeting_type,
            "description_coms": sem.description,
            "point_value_coms": sem.point_value
        }
        for sem in semesters
    ]

    return jsonify(semester_wics, semester_coms)