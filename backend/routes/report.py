import datetime
from backend import db
from flask import Blueprint, Flask, abort, render_template

report = Blueprint("report", __name__, static_folder="static/", template_folder="templates/")

@report.route("/admin/<int:org>")
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
        grad_students_year = db.Profile.query.filter(db.Profile.graduation_year == current_year).order_by(db.Profile.first_name, db.Profile.last_name).all()

        grad_students = [
            {
                "first_name": grad_student.first_name,
                "last_name": grad_student.last_name,
                "membership": grad_student.membership(org),
                "semesters": grad_student.semesters(org),
                "email_address": grad_student.email
            }
            for grad_student in grad_students_year
        ]

        # filters members that are active
        active_students = db.Profile.query.filter(db.Profile.membership(org) == 'active').order_by(db.Profile.semesters(org).desc()).all()

        active_student = [
            {
                "first_name": active.first_name,
                "last_name": active.last_name,
                "membership": active.membership(org),
                "semesters": active.semesters(org),
                "email_address": active.email
            }
            for active in active_students
        ]

        return render_template('database-view-wic.html.j2', active_count_members=active_count, inactive_count_members=inactive_count, 
                            alumni_count_members=alumni_count, graduation_students=grad_students, active=active_student)

    # COMs
    elif org == 2:
        # gets members
        active_count = db.Profile.query.filter(db.Profile.membership(org) == 'active').count() # added == 'active' because it was returning 0
        inactive_count = db.Profile.query.filter(db.Profile.membership(org) == 'inactive').count() # added == 'inactive' to match, actually got a different value, when it was ~ it was 505, with == 'inactive' it is 455
        alumni_count = db.Profile.query.filter(db.Profile.graduation_year < current_year).count()

        # filters members for grad year
        grad_students_year = db.Profile.query.filter(db.Profile.graduation_year == current_year).order_by(db.Profile.first_name, db.Profile.last_name).all()

        grad_students = [
            {
                "first_name": grad_student.first_name,
                "last_name": grad_student.last_name,
                "membership": grad_student.membership(org),
                "semesters": grad_student.semesters(org),
                "email_address": grad_student.email
            }
            for grad_student in grad_students_year
        ]

        # filters members that are active
        active_students = db.Profile.query.filter(db.Profile.membership(org) == 'active').order_by(db.Profile.semesters(org).desc()).all()

        active_student = [
            {
                "first_name": active.first_name,
                "last_name": active.last_name,
                "membership": active.membership(org),
                "semesters": active.semesters(org),
                "email_address": active.email
            }
            for active in active_students
        ]

        return render_template('database-view-coms.html.j2', active_count_members=active_count, inactive_count_members=inactive_count, 
                            alumni_count_memebers=alumni_count, graduation_students=grad_students, active=active_student)
    
    else:
        return abort(404)
