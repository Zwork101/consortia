from backend.db import Event, Profile
from flask import Blueprint, jsonify, request
from datetime import date

student = Blueprint("/student", __name__, static_folder="static/", template_folder="templates/")

@student.route("/meetings")
def upcoming_meetings():
    upcoming_meetings = Event.query.filter(Event.start_time >= date.today()).order_by(Event.start_time).all()
    meetings = [
        {
            "event_id": meeting.event_id,
            "meeting_type": meeting.meeting_type,
            "name": meeting.name,
            "start_time": meeting.start_time,
            "end_time": meeting.end_time,
            "description": meeting.description,
            "point_value": meeting.point_value,
            "organizer_id": meeting.organizer_id,
            "organizer": meeting.organizer,
            "attendants": meeting.attendants
        }
        for meeting in upcoming_meetings
    ]
    return jsonify(meetings)

@student.route("/attendance")
def member_attendance():
    profile_id = request.get_json()
    if not profile_id or "rit_id" not in profile_id:
        return jsonify({"error": "Missing rit_id in request"})

    id = profile_id.get("rit_id")
    attendance = Profile.query.filter(Profile.rit_id == id).all()
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