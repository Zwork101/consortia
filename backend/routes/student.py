from db import Event, Profile
from flask import Blueprint, jsonify
from datetime import date

student = Blueprint("/student", __name__, static_folder="static/", template_folder="templates/")

@student.route("/meetings")
def upcoming_meetings():
    upcoming_meetings = Event.query.filter(Event.start_time >= date.today).order_by(Event.start_time)
    meetings = [
        {
            "event_id": Event.event_id,
            "campus_group_id": Event.campus_group_id, 
            "meeting_type": Event.meeting_type,
            "name": Event.name,
            "start_time": Event.start_time,
            "end_time": Event.end_time,
            "description": Event.description,
            "point_value": Event.point_value,
            "organizer_id": Event.organizer_id,
            "organizer": Event.organizer,
            "attendance": Event.attendance
        }
        for meeting in upcoming_meetings
    ]
    return jsonify(meetings)

@student.route("/attendance")
def member_attendance():
    attendance = Profile.query(Profile.attendance)
    user_attendance = [
        {
            "profile_id": Profile.profile_id,
            "rit_id": Profile.rit_id,
            "last_name": Profile.last_name,
            "first_name": Profile.first_name,
            "attendance": Profile.attendance
        }
        for attendances in attendance
    ]
    return jsonify(user_attendance)

# just for the path of the site
#@student.route("/meeting/{id}")
#def meeting_id():
#    meeting_type = Event.query(Event.meeting_type)
#    event_type = Event.query.order_by(Event.event_id)