import datetime
from backend import db
from flask import Blueprint, Flask, abort, jsonify
from backend.auth import admin_required

report = Blueprint("report", __name__, static_folder="static/", template_folder="templates/")

@report.route("/admin/<int:org>/report")
@admin_required
def yearly_report(org: int):
    # year
    current_year = datetime.datetime.now().year

    # WIC
    if org == 1:
        # gets members
        active_count = db.Profile.query.filter(db.Profile.membership(org) == 'active').count() # added == 'active' because it was returning 0
        inactive_count = db.Profile.query.filter(db.Profile.membership(org) == 'inactive').count() # added == 'inactive' to match, actually got a different value, when it was ~ it was 505, with == 'inactive' it is 455
        alumni_count = db.Profile.query.filter(db.Profile.graduation_year < current_year).count()

        # filters members for grad year
        grad_member_year = db.Profile.query.filter(db.Profile.graduation_year == current_year).order_by(db.Profile.first_name, db.Profile.last_name).all()

        grad_members = [
            {
                "first_name": grad_member.first_name,
                "last_name": grad_member.last_name,
                "membership": grad_member.membership(org),
                "semesters": grad_member.semesters(org),
                "email_address": grad_member.email
            }
            for grad_member in grad_member_year
        ]

        # filters members that are active
        total_active_members = db.Profile.query.filter(db.Profile.membership(org) == 'active').order_by(db.Profile.semesters(org).desc()).all()

        active_members = [
            {
                "first_name": active_member.first_name,
                "last_name": active_member.last_name,
                "membership": active_member.membership(org),
                "semesters": active_member.semesters(org),
                "email_address": active_member.email
            }
            for active_member in total_active_members
        ]
    
        wic_student_data = {
            "active_count_members": active_count,
            "inactive_count_members": inactive_count,
            "alumni_count_members": alumni_count,
            "graduation_students": grad_members,
            "active_students": active_members
        }

        return jsonify(wic_student_data)

    # COMs
    elif org == 2:
        # gets members
        active_count = db.Profile.query.filter(db.Profile.membership(org) == 'active').count() # added == 'active' because it was returning 0
        inactive_count = db.Profile.query.filter(db.Profile.membership(org) == 'inactive').count() # added == 'inactive' to match, actually got a different value, when it was ~ it was 505, with == 'inactive' it is 455
        alumni_count = db.Profile.query.filter(db.Profile.graduation_year < current_year).count()

        # filters members for grad year
        grad_member_year = db.Profile.query.filter(db.Profile.graduation_year == current_year).order_by(db.Profile.first_name, db.Profile.last_name).all()

        grad_members = [
            {
                "first_name": grad_member.first_name,
                "last_name": grad_member.last_name,
                "membership": grad_member.membership(org),
                "semesters": grad_member.semesters(org),
                "email_address": grad_member.email
            }
            for grad_member in grad_member_year
        ]

        # filters members that are active
        total_active_members = db.Profile.query.filter(db.Profile.membership(org) == 'active').order_by(db.Profile.semesters(org).desc()).all()

        active_members = [
            {
                "first_name": active_member.first_name,
                "last_name": active_member.last_name,
                "membership": active_member.membership(org),
                "semesters": active_member.semesters(org),
                "email_address": active_member.email
            }
            for active_member in total_active_members
        ]

        coms_student_data = {
            "active_count_members": active_count,
            "inactive_count_members": inactive_count,
            "alumni_count_members": alumni_count,
            "graduation_students": grad_members,
            "active_students": active_members
        }

        return jsonify(coms_student_data)
    
    else:
        return abort(404)