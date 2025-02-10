import csv
import os

from backend.email import send_email
from backend.db import create_attendance, commit, Event, Profile, create_bonus

from flask import Blueprint, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Length


class CampusGroupsValidator:

    def __init__(self, parse_error_msg: str, invalid_fields_msg: str):
        self.parse_error_msg = parse_error_msg
        self.invalid_fields_msg = invalid_fields_msg

    def __call__(self, _: FlaskForm, field: FileField):
        reader = csv.DictReader(line.decode() for line in request.files[field.name])
        if "Email" not in reader.fieldnames:
            raise ValidationError(self.invalid_fields_msg)
        request.files[field.name].seek(0)  # Reset stream to start to re-read later
        

class AttendanceForm(FlaskForm):
    meeting_id = IntegerField("Meeting ID", validators=[DataRequired("Please provide a meeting ID")], render_kw = {'hidden': 'true'})
    csv_data = FileField("Data Upload", validators=[DataRequired("Please upload a CSV file with attendance data"), CampusGroupsValidator(
        "Unable to parse attendance file, ensure correct file was uploaded.",
        "Invalid fields in CSV file, missing 'Email' column. Ensure correct file was uploaded.",
    )])


class BonusForm(FlaskForm):
    giver_id = IntegerField("Giver ID", validators=[DataRequired("Please provide a profile ID to grant the points.")])
    point_value = IntegerField("Point Value", validators=[NumberRange(min=1, message="Please provide a point value greater than 0")])
    reason = StringField("Reason for points", validators=Length(min=2, max=500, message="Please keep the reason between 2 nad 500 characters."))
    

admin = Blueprint("admin", __name__, static_folder="static/", template_folder="templates/")


@admin.route("/meetings/upload", methods=["POST", "GET"])
def update_attendance_data():
    form = AttendanceForm()
    form.meeting_id.data = 8080

    if form.validate_on_submit():
        reader = csv.DictReader(line.decode() for line in request.files[form.csv_data.name])
        updated_users = []
        
        for row in reader:

            updated_users.append(
                create_attendance(row['Email'], form.meeting_id.data, row['First Name'], row['Last Name'])
            )
        
        commit(*updated_users)
        return f"Updated attendance records for {len(updated_users)} profiles."
    else:
        return render_template("upload-test.html", form=form)
    
@admin.route("/meetings/<int:meeting_id>/attendance")
def get_attendance_data(meeting_id: int):
    event = Event.query.get(meeting_id)
    if event is None:
        return 404
    
    try:
        skip = request.args.get("skip", 0, type = int)
        count = request.args.get("count", 100, type = int)
    except TypeError:
        return 400
    
    persons = event.attendants[skip:skip+count]
    
    return jsonify(
        [
            {
                "first_name": person.first_name,
                "last_name": person.last_name,
                "email": person.email
            } for person in persons
        ]
    )
    
@admin.route("/profile/<int:person_id>")
def get_profile_data(person_id: int):
    profile = Profile.query.get(person_id)
    if profile is None:
        return 404
    
    incomplete = profile.rit_id is None
    
    try:
        org = request.args.get("org_id", None, type = int)
    except TypeError:
        return 400
    
    base_profile_json = {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "email": profile.email,
            "attendance": [
                {
                    "event_id": event.event_id,
                    "name": event.name,
                    "description": event.description,
                    "meeting_type": event.meeting_type.value
                    
                } for event in profile.attendance if org is None or event.organizer_id == org
            ]
        }
    
    if incomplete:
        return jsonify({
            "incomplete": True,
            "profile": base_profile_json
        })
    else:
        base_profile_json.update({
            "rit_id": profile.rit_id,
            "graduation_year": profile.graduation_year,
            "degree": profile.degree,
            "pronouns": profile.pronouns,
            "avatar_path": profile.avatar_path,
            
            "awards": [
                {
                    "award_id": award.award_id,
                    "name": award.name,
                    "description": award.description,
                    "icon_path": award.icon_path        ,
                    "prize": award.prize            
                } for award in profile.awards if org is None or award.organization_id == org
            ],
            
            "administrator": None if not profile.administrator else profile.administrator.role.value
        })
        return jsonify({
            "incomplete": False,
            "profile": base_profile_json
        })
        

@admin.route("/profile/<int:person_id>/bonuses", methods=["POST"])
def grant_bonus(person_id: int):
    form = BonusForm()
    
    if form.validate_on_submit():
        create_bonus(
            form.point_value.data,
            person_id,
            form.giver_id.data,
            form.reason.data
        )
        commit()
        return 201
    return 400, "Unable to validate request"
        

@admin.route("/email")
def send_update():
    send_email(
        subject="This is an email test",
        body="Hello, I hope you received this email",
        sender=os.environ["EMAIL"],
        recipients=["njz8626@g.rit.edu"],
        password=os.environ["EMAIL_PASSWORD"]
    )
    return "Email sent!"