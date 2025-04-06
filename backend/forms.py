import csv

from flask import request
from flask_wtf import FlaskForm
from wtforms import EmailField, FileField, Form, IntegerField, StringField, SelectField, SubmitField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, NumberRange, Length

class NonValidatingSelectField(SelectField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """
    def pre_validate(self, form):
        pass


class CampusGroupsValidator:

    def __init__(self, parse_error_msg: str, invalid_fields_msg: str):
        self.parse_error_msg = parse_error_msg
        self.invalid_fields_msg = invalid_fields_msg

    def __call__(self, _: FlaskForm, field: FileField):
        reader = csv.DictReader(line.decode() for line in request.files[field.name])
        if reader.fieldnames is None or "Email" not in reader.fieldnames:
            raise ValidationError(self.invalid_fields_msg)
        request.files[field.name].seek(0)  # Reset stream to start to re-read later
        

class AttendanceForm(FlaskForm):
    meeting_id = NonValidatingSelectField("Meeting", validators=[DataRequired("Please provide a meeting ID")], choices=[("", "Select an Event")])
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


class EditUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired("Email is required"), Email(message="Invalid email address")])
    first_name = StringField("First Name", validators=[DataRequired("First name is required")])
    last_name = StringField("Last Name", validators=[DataRequired("Last name is required")])
    # rit_id = IntegerField("RIT ID (Optional)")
    graduation_year = IntegerField("Graduation Year (Optional)")
    degree = StringField("Degree (Optional)")
    pronouns = StringField("Pronouns (Optional)")
    # avatar_path = StringField("Avatar Path (Optional)")
    t_shirt_size = SelectField("Select a T-Shirt Size", choices=[
        ("Unset", "Unset"),
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"),
        ("X-Large", "X-Large"),
        ("XX-Large", "XX-Large"),
    ])
    submit = SubmitField("Update User")

    def validate_email(self, field):
        if not field.data.lower().endswith("@rit.edu"):
            raise ValidationError("Email must be a @rit.edu email address")


class SelectUserForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired("Please provide a user ID")])

# creates a search bar and searches rit id
class serachId(FlaskForm):
    rit_id = StringField("RIT ID", validators=[DataRequired("Please provide a RIT ID")], render_kw = {'hidden': 'true'})
    submit = SubmitField("Check RIT ID")


class BonusForm(FlaskForm):
    giver_id = IntegerField("Giver ID", validators=[DataRequired("Please provide a profile ID to grant the points."), DataRequired()])
    point_value = IntegerField("Point Value", validators=[NumberRange(min=1, message="Please provide a point value greater than 0"), DataRequired()])
    reason = StringField("Reason for points", validators=[Length(min=2, max=500, message="Please keep the reason between 2 and 500 characters."), DataRequired()])


class AwardForm(Form):
    award_id = HiddenField("Award ID")
    semester = IntegerField("Required Semesters", validators=[NumberRange(min=1), DataRequired()])
    award_name = StringField("Award Name", validators=[DataRequired(), Length(max=40)])

class WICConfigForm(FlaskForm):
    general_meetings_requirement = IntegerField("General Meetings Required", validators=[NumberRange(min=1), DataRequired()])
    committee_meetings_requirement = IntegerField("Committee Meetings Required", validators=[NumberRange(min=1), DataRequired()])
    social_meetings_requirement = IntegerField("Social Meetings Required", validators=[NumberRange(min=1), DataRequired()])
    volunteering_meetings_requirement = IntegerField("Volunteering Meetings Required", validators=[NumberRange(min=1), DataRequired()])
    award_settings = FieldList(FormField(AwardForm), "Awards per Semester")
    admins = FieldList(EmailField("Admins"))
