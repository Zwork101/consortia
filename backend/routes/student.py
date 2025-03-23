from backend.db import Event, Profile
from flask import Blueprint, jsonify, request
from datetime import date

student = Blueprint("/student", __name__, static_folder="static/", template_folder="templates/")

@student.route("/meetings")
def upcoming_meetings():
    """Return upcoming meetings based on pagination parameters."""
    try:
        skip = request.args.get("skip", 0, type=int)
        count = request.args.get("count", 9999, type=int)

        if skip < 0 or count <= 0:
            return jsonify({"Error": "Invalid pagination parameters"})
    except ValueError:
        return jsonify({"Error": "Invalid input type"})

    total_meetings = Event.query.filter(Event.start_time >= date.today()).count()
    meeting_results = (
        Event.query.filter(Event.start_time >= date.today())
        .order_by(Event.start_time)
        .offset(skip)
        .all()
    )

    meetings = [
        {
            "event_id": meeting.event_id,
            "meeting_type": meeting.meeting_type.value,  # Convert MeetingType to string
            "name": meeting.name,
            "start_time": meeting.start_time,
            "end_time": meeting.end_time,
            "description": meeting.description,
            "point_value": meeting.point_value,
            "organizer_id": meeting.organizer_id,
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