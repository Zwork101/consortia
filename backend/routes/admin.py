import csv
import os

from backend.email import send_email

from flask import Blueprint, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField
from wtforms.validators import DataRequired, ValidationError


class CampusGroupsValidator:

    def __init__(self, parse_error_msg: str, invalid_fields_msg: str, no_data_msg: str):
        self.parse_error_msg = parse_error_msg
        self.invalid_fields_msg = invalid_fields_msg
        self.no_data_msg = no_data_msg

    def __call__(self, _: FlaskForm, field: FileField):
        reader = csv.DictReader(request.FILES[field.name])
        if "Email" not in reader.fieldnames:
            raise ValidationError(self.invalid_fields_msg)
        if reader.line_num <= 1:
            raise ValidationError(self.no_data_msg)
        
        request.FILES[field.name].seek(0)  # Reset stream to start to re-read later
        

class AttendanceForm(FlaskForm):
    meeting_id = IntegerField("Meeting ID", validators=[DataRequired("Please provide a meeting ID")])
    csv_data = FileField("Data Upload", validators=[DataRequired("Please upload a CSV file with attendance data"), CampusGroupsValidator(
        "Unable to parse attendance file, ensure correct file was uploaded.",
        "Invalid fields in CSV file, missing 'Email' column. Ensure correct file was uploaded.",
        "Provided file contains no student data, no information to add."
    )])



admin = Blueprint("admin", __name__, static_folder="static/", template_folder="templates/")


@admin.route("/meetings/upload", methods=["PUT"])
def update_attendance_data():
    form = AttendanceForm()

    if form.validate_on_submit():
        reader = csv.DictReader(request.FILES[form.csv_data.name])
        for row in reader:
            pass  # TODO: Continue when database is finished


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