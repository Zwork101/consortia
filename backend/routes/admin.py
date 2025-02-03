import csv
import os

from backend.email import send_email
from backend.db import create_attendance, commit

from flask import Blueprint, request, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField
from wtforms.validators import DataRequired, ValidationError


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