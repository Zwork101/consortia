from datetime import datetime
import os
import logging
from time import sleep

from configs import update_org_settings
from backend.email import create_batches, generate_award_email, get_token, send_email
from backend.db import Administrator, Award, MeetingType, Organizations, ProfileAward, RoleType, award_user, create_attendance, commit, Event, Profile, create_bonus, db, make_admin
from backend.auth import admin_required
from backend.forms import CampusGroupsValidator, AttendanceForm, AddUserForm, EditUserForm, SelectUserForm, serachId, BonusForm, WICConfigForm, COMSConfigForm

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import current_user
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, delete

admin = Blueprint("admin", __name__, static_folder="static/", template_folder="templates/")

@admin.route("/admin/<int:org>")
@admin_required
def dashboard(org: int):
    if org == Organizations.WIC:
        return render_template("database-view-wic.html.j2", title="WIC Dashboard", upload_form=AttendanceForm(), org_id=org)
    elif org == Organizations.COMS:
        return render_template("database-view-coms.html.j2", title="COMS Dashboard", upload_form=AttendanceForm(), org_id=org)
    return abort(404)

@admin.route("/admin/<int:org>/settings", methods=["GET", "POST"])
@admin_required
def org_settings(org: int):
    org_awards = db.session.query(Award.award_id, Award.name, Award.active_semester_requirements).where(Award.organization_id == org).all()
    admins = db.session.query(Profile.email).select_from(Administrator).join(Profile, Administrator.profile_id == Profile.profile_id).where(Administrator.organization_id == org).all()

    if org == Organizations.WIC:
        form = WICConfigForm(
            **current_app.config["ORG_SETTINGS"][str(org)],
            award_settings=[
            {"award_id": award[0], "semester": award[2], "award_name": award[1]}
            for award in org_awards],
            admins=map(lambda x: x[0], admins)
        )
    elif org == Organizations.COMS:
        form = COMSConfigForm(
            **current_app.config["ORG_SETTINGS"][str(org)],
            award_settings=[
            {"award_id": award[0], "semester": award[2], "award_name": award[1]}
            for award in org_awards],
            admins=map(lambda x: x[0], admins)
        )
    else:
        abort(404)



    if form.validate_on_submit():
        if org == Organizations.WIC:
            update_org_settings(org, 
                general_meetings_requirement = form.general_meetings_requirement.data,
                committee_meetings_requirement = form.committee_meetings_requirement.data,
                social_meetings_requirement = form.social_meetings_requirement.data,
                volunteering_meetings_requirement = form.volunteering_meetings_requirement.data
            )
        elif org == Organizations.COMS:
            update_org_settings(org,
                attendance = [
                    {"percent": requirement.percent.data, "points": requirement.points.data}
                for requirement in form.attendance],
                volunteer = [
                    {"threshold": requirement.threshold.data, "points": requirement.points.data}
                for requirement in form.volunteer],
                mentorship_minimum = form.mentorship_minimum.data,
                mentorship_maximum = form.mentorship_maximum.data,
                required_points = form.required_points.data
            )

        for award in org_awards:
            if award[0] not in map(lambda x: x.award_id.data, form.award_settings):
                db.session.query(Award).where(Award.award_id == award[0]).delete()

        for new_award in form.award_settings:
            existing_award = next((oa for oa in org_awards if oa[0] == new_award.award_id.data), None)
            if existing_award is None:
                db.session.add(
                    Award(
                        name = new_award.award_name.data,
                        organization_id = org,
                        active_semester_requirements = new_award.semester.data
                    )
                )
            else:
                if existing_award[2] != new_award.semester.data or existing_award[1] != new_award.award_name.data:
                    award = db.session.get_one(Award, existing_award[0])
                    award.active_semester_requirements = new_award.semester.data
                    award.name = new_award.award_name.data

        removed_admins = [admin[0] for admin in admins if admin not in form.admins.data]
        admins_to_remove = db.session.query(Administrator).join(Profile).where(Profile.email.in_(removed_admins))
        for admin in admins_to_remove:
            db.session.delete(admin)
        new_admins = [admin for admin in form.admins.data if admin not in admins]
        for admin in new_admins:
            user_id = db.session.query(Profile.profile_id).where(Profile.email == admin).one_or_none()
            if user_id is not None:
                make_admin(user_id[0], org, RoleType.ADMIN)

        commit()

        return redirect(
            url_for("admin.org_settings", org=org)
        )

    for fieldName, errorMessages in form.errors.items():
        print(fieldName, errorMessages)

    if org == Organizations.WIC:
        return render_template("configuration-wics.html.j2", title="WiC Configuration", org_id=org, form=form)
    elif org == Organizations.COMS:
        return render_template("configuration-coms.html.j2", title="COMS Configuration", org_id=org, form=form)

@admin.route("/admin/<int:org>/create", methods=["POST"])
@admin_required
def create_event(org: int):
    meeting_org = org
    meeting_name = request.form.get("meeting_name")
    meeting_description = request.form.get("meeting_description")
    meeting_start_time = request.form.get("meeting_start_time")
    meeting_end_time = request.form.get("meeting_end_time")
    meeting_location = request.form.get("meeting_location")
    
    db.session.add(Event(
        name=meeting_name,
        description=meeting_description,
        start_time=meeting_start_time,
        end_time=meeting_end_time,
        location=meeting_location,
        organizer_id=meeting_org
    ))
    db.session.commit()
    return redirect(url_for("admin.dashboard", org=org))
    

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

@admin.route("/admin/profiles/<int:org>", methods=["GET"])
@admin_required
def list_users(org: int):
    try:
        skip = request.args.get("skip", 0, type=int)
        count = request.args.get("count", 100, type=int)
        sort_by = request.args.get("filter-sort-by", "first_name")
        sort_order = request.args.get("filter-sort-order", "Ascending")
        membership_filter = request.args.get("filter-membership", "All")
        semesters_filter = request.args.get("filter-semesters", "All")
        search_query = request.args.get("search", None)
    except TypeError:
        raise
    
    # Base query: only profiles with attendance in given org
    query = Profile.query.filter(Profile.attendance.any(Event.organizer_id == org))
    query = db.session.query(
        Profile.first_name,
        Profile.last_name,
        Profile.membership(org),
        Profile.semesters(org),
        Profile.email,
        Profile.count_attendance(org, MeetingType.GENERAL),
        Profile.count_attendance(org, MeetingType.COMMITTEE),
        Profile.count_attendance(org, MeetingType.SOCIAL),
        Profile.count_attendance(org, MeetingType.VOLUNTEER)
    )
    
    # Apply membership filter if requested.
    if membership_filter != "All":
        if membership_filter == "Non-Active Member":
            query = query.filter(Profile.membership_sql(org) == "inactive")
        elif membership_filter == "Active Member":
            query = query.filter(Profile.membership_sql(org) == "active")
    
    # Filter on semesters if selected.
    if semesters_filter != "All":
        if semesters_filter == "None":
            query = query.filter(Profile.semesters_sql(org) == 0)
        else:
            query = query.filter(Profile.semesters_sql(org) > 0)
    
    # Apply text search filter on first name, last name, and email.
    if search_query:
        query = query.filter(
            or_(
                Profile.first_name.ilike(f"%{search_query}%"),
                Profile.last_name.ilike(f"%{search_query}%"),
                Profile.email.ilike(f"%{search_query}%")
            )
        )
    
    # Determine sort column - only for allowed sortable columns
    # Map the frontend sort keys to actual model attributes
    sort_column_map = {
        "first_name": Profile.first_name,
        "last_name": Profile.last_name,
        "email": Profile.email,
        "semesters": Profile.semesters_sql(org),
        "points": Profile.points(org)
        # Removed 'membership' from sortable columns
    }
    
    # Get the sort column or default to first_name
    sort_column = sort_column_map.get(sort_by.lower(), Profile.first_name)
    
    # Apply sort direction
    if sort_order.lower().startswith("desc"):
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()
    
    users = query.order_by(sort_column).limit(count).offset(skip).all()

    print(users)

    return jsonify([
        {"profile": user.serialize(org)["profile"]}
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

    # Update basic profile data
    user.email = request.form.get("email")
    user.first_name = request.form.get("first_name")
    user.last_name = request.form.get("last_name")
    user.rit_id = request.form.get("rit_id", type=int)
    user.graduation_year = request.form.get("graduation_year", type=int)
    user.degree = request.form.get("degree")
    user.pronouns = request.form.get("pronouns")
    user.avatar_path = request.form.get("avatar_path")
    
    org_id = request.form.get("organization_id", type=int) or Organizations.COMS

    # Process bonus points for COMS profiles if provided
    bonus_points = request.form.get("bonus_points", type=int)
    bonus_reason = request.form.get("bonus_reason")
    if org_id == Organizations.COMS and bonus_points and bonus_reason:
        create_bonus(
            bonus_points,
            user.profile_id,
            current_user.profile_id,
            bonus_reason,
            org_id
        )
    
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

@admin.route("/admin/profiles/<int:org>/worthy")
@admin_required
def worthy_members(org: int):
    # This code is so, so bad. And so slow :(
    org_profiles = db.session.query(Profile) \
                        .filter(Profile.semesters(org) > 0) \
                        .all()

    awards = []
    awards_db = []

    reached_active = [p for p in org_profiles if p.membership_sql(org)]

    for profile in reached_active:
        award = db.session.query(Award.award_id, Award.name, Award.active_semester_requirements)\
            .filter(Award.active_semester_requirements == profile.membership_semesters(org))\
            .filter(Award.organization_id == org)\
            .first()
        if award:
            awards.append((profile, award))
            awards_db.append(
                ProfileAward(profile_id=profile.profile_id, award_id=award.award_id, award_date=datetime.now())
            )

    commit(*awards_db)
    return jsonify([
        {
            "profile_id": award[0].profile_id,
            "first_name": award[0].first_name,
            "last_name": award[0].last_name,
            "award_id": award[1][0],
            "award_name": award[1][1],
            "award_requirement": award[1][2]
        } for award in awards
    ])

@admin.route("/admin/awards/<int:org>/notify", methods=["POST"])
@admin_required
def send_awards(org: int):
    selected_users = request.get_json()
    awards = []
    
    for user in selected_users:
        awards.append(award_user(user['award_id'], user['profile_id']))

    commit(*awards)

    profiles = [Profile.query.get(int(u['profile_id'])) for u in selected_users]
    awards = [Award.query.get(int(u['award_id'])) for u in selected_users]

    emails = []

    for profile, award in zip(profiles, awards):
        emails.append(
            generate_award_email(profile, award, org)
        )

    cred_emails = get_token(org)

    if not cred_emails:
        return jsonify({
            "success": False,
            "url": url_for("oauth.authorize_email", org=org)
            })

    for i, batch in enumerate(create_batches(emails, cred_emails[1], cred_emails[0], "You've earned a reward!")):
        if i != 0:
            sleep(2)
        batch.execute()

    return jsonify({
        "success": True
    })

@admin.route("/admin/events/<int:org>", methods=["GET"])
@admin_required
def list_events(org: int):
    # Get sorting parameters
    sort_by = request.args.get("filter-sort-by", "date")
    sort_order = request.args.get("filter-sort-order", "Descending")
    
    # Count profiles that have attended any event for this org
    total_profiles = Profile.query.filter(Profile.attendance.any(Event.organizer_id == org)).count()
    
    # Base query
    query = Event.query.filter_by(organizer_id=org)
    
    # Map frontend sort keys to actual model attributes
    sort_column_map = {
        "name": Event.name,
        "date": Event.start_time
    }
    
    # Get the sort column
    sort_column = sort_column_map.get(sort_by.lower(), Event.start_time)
    
    # Apply sort direction
    if sort_order.lower().startswith("desc"):
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    events = query.all()
    
    result = []
    for event in events:
        attendees = len(event.attendants)
        percentage = (attendees / total_profiles * 100) if total_profiles > 0 else 0
        result.append({
            "event_id": event.event_id,
            "name": event.name,
            "type": event.meeting_type.value, 
            "description": event.description,
            "location": event.location,
            "start_time": event.start_time.isoformat(),
            "attendance_count": attendees,
            "attendance_percentage": round(percentage)
        })
    
    # For attendance_count and percentage sorting, we need to sort the result list
    if sort_by.lower() in ["attendees", "percentage"]:
        sort_key = "attendance_count" if sort_by.lower() == "attendees" else "attendance_percentage"
        reverse = sort_order.lower().startswith("desc")
        result.sort(key=lambda x: x[sort_key], reverse=reverse)
    
    return jsonify(result)
