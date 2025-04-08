from datetime import datetime
from os import curdir

from backend.db import Event, Profile, commit, db, Administrator, Award
from backend.forms import EditUserForm

from flask_login import current_user
from flask import Blueprint, abort, current_app, jsonify, redirect, request, render_template, url_for

student = Blueprint("student", __name__, static_folder="static/", template_folder="templates/")

@student.route("/wic")
def wic_homepage():
    return render_template("wics-profile.html.j2", title="WIC", org=1)

@student.route("/coms")
def coms_homepage():
    return render_template("coms-profile.html.j2", title="COMS", org=2)

@student.route("/settings/<int:org>")
def provide_org_config(org: int):
    org_awards = db.session.query(Award.award_id, Award.name, Award.active_semester_requirements).where(Award.organization_id == org).all()
    admins = db.session.query(Profile.email, Profile.first_name, Profile.last_name)\
        .select_from(Administrator)\
        .join(Profile, Administrator.profile_id == Profile.profile_id)\
        .where(Administrator.organization_id == org).all()

    return jsonify({
        "config": current_app.config["ORG_SETTINGS"][str(org)],
        "awards": [{
            "award_id": award[0],
            "award_name": award[1],
            "semester_requirement": award[2]
        } for award in org_awards],
        "admins": [{
            "admin_name": admin[1] + " " + admin[2],
            "admin_email": admin[0]
        } for admin in admins]
    })

@student.route("/profile", methods=["GET"])
def return_profile():
    org = request.args.get("org", type=int)
    if org:
        return current_user.serialize(org)
    else:
        return current_user.serialize()
    return abort(403)

@student.route("/meetings/<int:org>")
def upcoming_meetings(org: int):
    """Return upcoming meetings based on pagination parameters."""
    try:
        skip = request.args.get("skip", 0, type=int)
        #count = request.args.get("count", 9999, type=int)
        count = request.args.get("count", 3, type=int)

        if skip < 0 or count <= 0:
            return jsonify({"Error": "Invalid pagination parameters"})
    except ValueError:
        return jsonify({"Error": "Invalid input type"})

    current_time = datetime.now()
    
    meeting_results = (
        Event.query
        .filter(Event.organizer_id == org, Event.start_time >= current_time)
        .order_by(Event.start_time)
        .offset(skip)
        .limit(count)
        .all()
    )

    # meeting_results = (
    #     Event.query.filter(Event.organizer_id == org)
    #     .order_by(Event.start_time)
    #     .offset(skip)
    #     .all()
    # )

    meetings = [
        {
            "event_id": meeting.event_id,
            "meeting_type": meeting.meeting_type.value,
            "name": meeting.name,
            "start_time": meeting.start_time.isoformat(),
            "end_time": meeting.end_time.isoformat(),
            "location": meeting.description,
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
    #old good
    #return jsonify({"Meetings": meetings})
    #new bad
    return render_template("wics-profile.html.j2", meetings=meeting_results)

@student.route("/attendance")
def member_attendance():  # What is going on in this function??
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
# Reused from admin.py... 

@student.route("/account", methods=["POST", "GET"])
def account():
    form = EditUserForm(
        graduation_year=current_user.graduation_year,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        degree=current_user.degree,
        pronouns=current_user.pronouns,
        t_shirt_size=current_user.t_shirt_size if current_user.t_shirt_size else "Unset",
        email=current_user.email
    )

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.graduation_year = form.graduation_year.data
        current_user.degree = form.degree.data
        current_user.pronouns = form.pronouns.data
        if form.t_shirt_size.data != "Unset":
            current_user.t_shirt_size = form.t_shirt_size.data
        commit(current_user)
        return redirect(url_for("student.account"))
    
    return render_template("student-profile.html.j2", title="Student Profile", form=form)
