import csv
import os

from backend.email import send_email
from backend.db import create_attendance, commit, Event, Profile

from flask import Blueprint, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError, Email

from backend.db import Event, commit, create_attendance, Profile, db
from backend.email import send_email

from sqlalchemy.orm import Session


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


class AddUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired("Email is required"), Email(message="Invalid email address")])
    first_name = StringField("First Name", validators=[DataRequired("First name is required")])
    last_name = StringField("Last Name", validators=[DataRequired("Last name is required")])
    rit_id = IntegerField("RIT ID (Optional)")
    graduation_year = IntegerField("Graduation Year (Optional)")
    degree = StringField("Degree (Optional)")
    pronouns = StringField("Pronouns (Optional)")
    avatar_path = StringField("Avatar Path (Optional)")

    def validate_email(self, field):
        if not field.data.lower().endswith("@rit.edu"):
            raise ValidationError("Email must be a @rit.edu email address")


class DeleteUserForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired("Please provide a user ID")])

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
        return jsonify({
            "msg": f"Updated attendance records for {len(updated_users)} profiles."
        })
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
        
    try:
        org = request.args.get("org_id", None, type = int)
    except TypeError:
        return 400
    
    return jsonify({
        profile.serialize(org)
    })
        


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


@admin.route("/admin/profiles/<int:organization>", methods=["GET"])
def list_users(organization: int):

    try:
        skip = request.args.get("skip", 0, type = int)
        count = request.args.get("count", 100, type = int)
    except TypeError:
        return 400

    rows = db.session.query(Profile, Event).filter(
        Event.organizer_id == organization
    ).limit(count).offset(skip).all()

    users: list[Profile] = []
    for row in rows:
        if row[0] not in users:
            users.append(row[0])

    return jsonify([
        user.serialize(organization) for user in users
    ])


@admin.route("/admin/add_user", methods=["GET", "POST"])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        new_user = Profile(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            rit_id=form.rit_id.data,
            graduation_year=form.graduation_year.data,
            degree=form.degree.data,
            pronouns=form.pronouns.data,
            avatar_path=form.avatar_path.data
        )
        db.session.add(new_user)
        db.session.commit()
        return f"User {new_user.first_name} {new_user.last_name} added successfully."
    return render_template("add-user.html", form=form)


@admin.route("/admin/delete_user", methods=["GET", "POST"])
def delete_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        user = Profile.query.get(form.user_id.data)
        if user:
            db.session.delete(user)
            db.session.commit()
            return f"User with ID {form.user_id.data} deleted successfully."
        else:
            return f"No user found with ID {form.user_id.data}."
    return render_template("delete-user.html", form=form)