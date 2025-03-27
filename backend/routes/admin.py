import csv
import os
import logging

from backend.email import send_email
from backend.db import Organizations, create_attendance, commit, Event, Profile, create_bonus
from backend.auth import admin_required

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, abort
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import FileField, IntegerField, StringField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email

from backend.db import Event, commit, create_attendance, Profile, db

from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from wtforms import FileField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Length


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
    rit_id = IntegerField("RIT ID (Optional)")
    graduation_year = IntegerField("Graduation Year (Optional)")
    degree = StringField("Degree (Optional)")
    pronouns = StringField("Pronouns (Optional)")
    avatar_path = StringField("Avatar Path (Optional)")
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


admin = Blueprint("admin", __name__, static_folder="static/", template_folder="templates/")

@admin.route("/admin/<int:org>")
@admin_required
def dashboard(org: int):
    if org == Organizations.WIC:
        return render_template("database-view-wic.html.j2", title="WIC Dashboard", upload_form=AttendanceForm())
    elif org == Organizations.COMS:
        return render_template("database-view-coms.html.j2", title="COMS Dashboard", upload_form=AttendanceForm())


@admin.route("/meetings/<int:org>/upload", methods=["POST", "GET"])
@admin_required
def update_attendance_data(org: int):
    form = AttendanceForm()

    if form.validate_on_submit():
        valid_meeting = db.session.query(Event.event_id).select_from(Event).where(Event.organizer_id == org).where(Event.event_id == form.meeting_id.data)
        if valid_meeting.first() is None:
            return abort(404)

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
    

@admin.route("/meetings/<int:org>/<int:meeting_id>/attendance")
@admin_required
def get_attendance_data(org:int, meeting_id: int):
    event = Event.query.get(meeting_id)

    if event is None:
        return abort(404)

    if event.organizer_id != org:
        abort(403)
    
    try:
        skip = request.args.get("skip", 0, type = int)
        count = request.args.get("count", 100, type = int)
    except TypeError:
        return abort(400)
    
    persons = event.attendants[skip:skip+count]
    
    return jsonify(
        [
            {
                "first_name": person.first_name,
                "last_name": person.last_name,
                "email": person.email,
                "id": person.profile_id
            } for person in persons
        ]
    )
    
@admin.route("/profile/<int:org>/<int:person_id>")
@admin_required
def get_profile_data(org:int, person_id: int):
    profile = Profile.query.get(person_id)
    if profile is None:
        return abort(404)
    
    return jsonify(
        profile.serialize(org)
    )
        

@admin.route("/profile/<int:org>/<int:person_id>/bonuses", methods=["POST"])
@admin_required
def grant_bonus(org: int, person_id: int):
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

# search for id in the meetings attendance
@admin.route("/search", methods=['POST'])
def id_search():
    form = serachId()
    filtered_data = None
    
    if form.validate_on_submit():
        search_query = request.args.get('search')
        filtered_data = Event.query.filter(
            or_(
                Event.name.ilike(f"%{search_query}%"),
                Event.description.ilike(f"%{search_query}%")
            )).all()
        return render_template('/', form = form, data = filtered_data)
    
    abort(200)

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
        skip = request.args.get("skip", 0, type=int)
        count = request.args.get("count", 100, type=int)
        sort_by = request.args.get("filter-sort-by", "First Name")
        sort_order = request.args.get("filter-sort-order", "Ascending")
        membership_filter = request.args.get("filter-membership", "All")
        semesters_filter = request.args.get("filter-semesters", "All")
        search_query = request.args.get("search", None)
    except TypeError:
        raise
    
    # Base query: only profiles with attendance in given org
    query = Profile.query.filter(Profile.attendance.any(Event.organizer_id == organization))
    
    # Apply membership filter if requested.
    if membership_filter != "All":
        if membership_filter == "Non-Active Member":
            query = query.filter(Profile.membership_sql(organization) == "inactive")
        elif membership_filter == "Active Member":
            query = query.filter(Profile.membership_sql(organization) == "active")
    
    # Filter on semesters if selected.
    if semesters_filter != "All":
        if semesters_filter == "None":
            query = query.filter(Profile.semesters_sql(organization) == 0)
        else:
            query = query.filter(Profile.semesters_sql(organization) > 0)
    
    # Apply text search filter on first name, last name, and email.
    if search_query:
        query = query.filter(
            or_(
                Profile.first_name.ilike(f"%{search_query}%"),
                Profile.last_name.ilike(f"%{search_query}%"),
                Profile.email.ilike(f"%{search_query}%")
            )
        )
    
    # Determine sort column.
    if sort_by.lower() == "first name":
        sort_column = Profile.first_name
    elif sort_by.lower() == "last name":
        sort_column = Profile.last_name
    else:
        sort_column = Profile.first_name
    
    if sort_order.lower().startswith("desc"):
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()
    
    users = query.order_by(sort_column).limit(count).offset(skip).all()
    return jsonify([
        {"profile": user.serialize(organization)["profile"]}
        for user in users
    ])


@admin.route("/admin/add_user", methods=["GET", "POST"])
@admin_required
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


@admin.route("/admin/select_user", methods=["GET", "POST"])
@admin_required
def select_user():
    form = SelectUserForm()
    if form.validate_on_submit():
        user = Profile.query.get(form.user_id.data)
        if user:
            return redirect(url_for('admin.edit_user', user_id=user.profile_id))
        else:
            return f"No user found with ID {form.user_id.data}."
    return render_template("select-user.html", form=form)

@admin.route("/admin/edit_user", methods=["GET", "POST"])
@admin_required
def edit_user():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return "User ID required", 400

    user = Profile.query.get(user_id)
    if not user:
        return f"No user found with ID {user_id}", 404

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        # Gather updated data without committing yet.
        updated_data = {
            "email": form.email.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "rit_id": form.rit_id.data,
            "graduation_year": form.graduation_year.data,
            "degree": form.degree.data,
            "pronouns": form.pronouns.data,
            "avatar_path": form.avatar_path.data,
        }
        # Pass both original and updated data to confirmation view.
        return render_template("edit-user-confirmation.html",
                               user=user,
                               updated_data=updated_data)
    # GET: render form prepopulated with user's current data.
    return render_template("edit-user.html", form=form, user=user)

@admin.route("/admin/edit_user/confirm", methods=["POST"])
@admin_required
def confirm_edit_user():
    user_id = request.form.get("user_id", type=int)
    if not user_id:
        return "User ID required", 400

    user = Profile.query.get(user_id)
    if not user:
        return f"No user found with ID {user_id}", 404

    # The confirmation form submits updated fields as hidden values.
    user.email = request.form.get("email")
    user.first_name = request.form.get("first_name")
    user.last_name = request.form.get("last_name")
    user.rit_id = request.form.get("rit_id", type=int)
    user.graduation_year = request.form.get("graduation_year", type=int)
    user.degree = request.form.get("degree")
    user.pronouns = request.form.get("pronouns")
    user.avatar_path = request.form.get("avatar_path")

    org_id = request.form.get("organization_id", type=int) or Organizations.COMS
    
    db.session.commit()
    flash("User updated successfully.")
    return redirect(url_for("admin.dashboard", org=org_id))

@admin.route("/admin/delete_user", methods=["GET", "POST"])
@admin_required
def delete_user():
    if request.method == "GET":
        user_id = request.args.get("user_id", type=int)
        if not user_id:
            return "User ID required", 400
        user = Profile.query.get(user_id)
        if not user:
            return f"No user found with ID {user_id}", 404
        return render_template("confirm-delete-user.html", user=user)
    else:
        user_id = request.form.get("user_id", type=int)
        if not user_id:
            return "User ID required", 400
        user = Profile.query.get(user_id)
        if not user:
            return f"No user found with ID {user_id}", 404
        # If user has an associated administrator, delete it first.
        if user.administrator:
            db.session.delete(user.administrator)
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully.")
        return redirect(url_for("admin.admin_interface"))
