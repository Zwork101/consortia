from datetime import datetime, timedelta, timezone
from enum import Enum as EnumClass
from types import MethodType
from typing import Any, Optional
import logging

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import foreign, mapper, relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, Table, Column, func, case, cast, and_


class MeetingType(EnumClass):
    GENERAL = "GENERAL"
    VOLUNTEER = "VOLUNTEER"
    SOCIAL = "SOCIAL"
    COMMITTEE = "COMMITTEE"
    MENTORSHIP = "MENTORSHIP"


class RoleType(EnumClass):
    ADMIN = "ADMIN"
    PLANNER = "PLANNER"


class Organizations:
    WIC = 1
    COMS = 2
    
    
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


attendance_table = Table(
    "attendance",
    Base.metadata,
    Column("profile_id", ForeignKey("Profile.profile_id"), nullable=False),
    Column("event_id", ForeignKey("Event.event_id"), nullable=False),
    Column("hours", type_=Integer, default=0)
)

# class Attendance(db.Model):
#     __tablename__ = "attendance"
#     __table_args__ = {'extend_existing': True}

#     profile_id: Mapped[int] = relationship("Profile", foreign_keys="[Profile.profile_id]")
#     event_id: Mapped[int] = relationship("Event", foreign_keys="[Event.profile_id]")
#     hours: Mapped[int] = mapped_column(default=0)


class Profile(db.Model, UserMixin):
    __tablename__ = 'Profile'

    profile_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    rit_id: Mapped[Optional[str]]
    last_name: Mapped[str]
    first_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    graduation_year: Mapped[Optional[int]]
    degree: Mapped[Optional[str]]
    pronouns: Mapped[Optional[str]]
    avatar_path: Mapped[Optional[str]]
    t_shirt_size: Mapped[Optional[str]]

    attendance: Mapped[list["Event"]] = relationship(secondary=attendance_table, back_populates="attendants")
    awards: Mapped[list["Award"]] = relationship(secondary="ProfileAward", back_populates="recipients")
    positions: Mapped[list["Administrator"]] = relationship("Administrator", foreign_keys="[Administrator.profile_id]", back_populates="profile")
    bonuses: Mapped[list["BonusPoints"]] = relationship("BonusPoints", foreign_keys="[BonusPoints.recipient_id]", back_populates="recipient")
    grants: Mapped[list["BonusPoints"]] = relationship("BonusPoints", foreign_keys="[BonusPoints.giver_id]", back_populates="giver")
    
    # @hybrid_method
    # def membership(self, org: int):
    #     count = 0
    #     for event in self.attendance:
    #         if event.end_time.replace(tzinfo=timezone.utc) > (datetime.now(timezone.utc) - timedelta(weeks=10)) and event.organizer_id == org:
    #             count += 1
    #     return 'active' if count > 5 else ('inactive' if count == 0 else 'incomplete')
    
    # @membership.expression
    # def membership_sql(cls, org: int):
    #     query = db.session.query(func.count(attendance_table.c.event_id))\
    #         .join(Event, Event.event_id == attendance_table.c.event_id)\
    #         .where(attendance_table.c.profile_id == cls.profile_id)\
    #         .where(Event.organizer_id == org)\
    #         .where(Event.end_time > (datetime.utcnow() - timedelta(weeks=10)))\
    #         .scalar_subquery()
            
    #     return case(
    #         (query > 5, "Member"),
    #         else_ = "Non-Member"
    #     )

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.profile_id)
    
    @hybrid_method
    def membership(self, org: int, current_semester = None):
        if current_semester is None:
            current_semester = (datetime.now(timezone.utc).year * 10) + ((datetime.now(timezone.utc).month // 7) * 5)
        
        if org == Organizations.WIC:
            general_meetings = 0
            committee = 0
            social_event = 0
            volunteer = 0

            # Get current semester events for WIC
            for event in [e for e in self.attendance if e.semester == current_semester]:
                if event.meeting_type == MeetingType.GENERAL:
                    general_meetings += 1
                elif event.meeting_type == MeetingType.COMMITTEE:
                    committee += 1
                elif event.meeting_type == MeetingType.SOCIAL:
                    social_event += 1
                elif event.meeting_type == MeetingType.VOLUNTEER:
                    volunteer += 1

            return (general_meetings >= 14) and (committee >= 6) and (volunteer >= 1) and (social_event >= 1)
        
        elif org == Organizations.COMS:
            # Get current semester events for COMS
            org_events = [e for e in self.attendance if (e.organizer_id == org and e.semester == current_semester)]
            print(f"Org Events: {org_events}")
            total_points = 0
            
            # General meeting attendance points
            total_general_meetings = Event.query.filter_by(
                organizer_id=org, 
                meeting_type=MeetingType.GENERAL,
                semester=current_semester
            ).count()

            print(f"Total General: {total_general_meetings}")
            
            if total_general_meetings > 0:
                attended_meetings = len([e for e in org_events if e.meeting_type == MeetingType.GENERAL])
                attendance_percent = (attended_meetings / total_general_meetings) * 100
                
                if attendance_percent >= 100:
                    total_points += 3
                elif attendance_percent >= 75:
                    total_points += 2
                elif attendance_percent >= 50:
                    total_points += 1

                print(f"General Attended: {attended_meetings}")
            
            # Volunteer work points
            volunteer_hours = 0
                
            for e in org_events:

                if e.meeting_type == MeetingType.VOLUNTEER:
                    print(e.name, e.get_hours(self.profile_id))
                    volunteer_hours += e.get_hours(self.profile_id)

            print(volunteer_hours)
            
            if volunteer_hours >= 9:
                total_points += 4
            elif volunteer_hours >= 6:
                total_points += 3
            elif volunteer_hours >= 3:
                total_points += 2
            elif volunteer_hours >= 1:
                total_points += 1
            
            # Mentorship program points
            mentorship_meetings = [e for e in org_events if e.meeting_type == MeetingType.MENTORSHIP]
            if mentorship_meetings:
                # Base 3 points for being in the program
                mentorship_points = 3 + len(mentorship_meetings)
                # Cap at 9 points
                total_points += min(mentorship_points, 9)

                print(f"Mentor Points: {len(mentorship_meetings)}")
            
            # Add bonus points from miscellaneous contributions
            total_points += self.bonus_points(org)
            
            # Return True if they have 16 or more points
            return total_points >= 16
        else:
            raise ValueError(f"Unknown Organization: {org}")

    @membership.expression
    @classmethod
    def membership_sql(cls, org: int):
        current_semester = (datetime.now(timezone.utc).year * 10) + ((datetime.now(timezone.utc).month // 7) * 5)
        
        if org == Organizations.WIC:
            general_meeting_query = db.session.query(func.count(Event.event_id))\
                .select_from(Event)\
                .join(attendance_table, Event.event_id == attendance_table.c.event_id)\
                .where(attendance_table.c.profile_id == cls.profile_id)\
                .where(Event.semester == current_semester)\
                .where(Event.meeting_type == MeetingType.GENERAL)\
                .scalar_subquery()

            committee_meeting_query = db.session.query(func.count())\
                .select_from(Event)\
                .join(attendance_table, Event.event_id == attendance_table.c.event_id)\
                .where(attendance_table.c.profile_id == cls.profile_id)\
                .where(Event.semester == current_semester)\
                .where(Event.meeting_type == MeetingType.COMMITTEE)\
                .scalar_subquery()

            social_meeting_query = db.session.query(func.count())\
                .select_from(Event)\
                .join(attendance_table, Event.event_id == attendance_table.c.event_id)\
                .where(attendance_table.c.profile_id == cls.profile_id)\
                .where(Event.semester == current_semester)\
                .where(Event.meeting_type == MeetingType.SOCIAL)\
                .scalar_subquery()

            volunteer_meeting_query = db.session.query(func.count())\
                .select_from(Event)\
                .join(attendance_table, Event.event_id == attendance_table.c.event_id)\
                .where(attendance_table.c.profile_id == cls.profile_id)\
                .where(Event.semester == current_semester)\
                .where(Event.meeting_type == MeetingType.VOLUNTEER)\
                .scalar_subquery()

            return case(
                ((general_meeting_query >= 14) & (committee_meeting_query >= 6) & (social_meeting_query >= 1) & (volunteer_meeting_query >= 1), "active"),
                else_="inactive"
            )
        
        elif org == Organizations.COMS:
            # Get total general meetings for the semester
            total_general_meetings = db.session.query(func.count(Event.event_id))\
                .where(Event.organizer_id == org)\
                .where(Event.semester == current_semester)\
                .where(Event.meeting_type == MeetingType.GENERAL)\
                .scalar_subquery()
            
            # Calculate attended general meetings
            attended_general_meetings = db.session.query(func.count(Event.event_id))\
                .select_from(Event)\
                .join(attendance_table, Event.event_id == attendance_table.c.event_id)\
                .where(attendance_table.c.profile_id == cls.profile_id)\
                .where(Event.organizer_id == org)\
                .where(Event.semester == current_semester)\
                .where(Event.meeting_type == MeetingType.GENERAL)\
                .scalar_subquery()
            
            # Calculate attendance percentage
            attendance_percent = case(
                (total_general_meetings > 0, (cast(attended_general_meetings * 100, Integer) / total_general_meetings)),
                else_=0
            )
            
            # Calculate general meeting points
            general_meeting_points = case(
                (attendance_percent >= 100, 3),
                (attendance_percent >= 75, 2),
                (attendance_percent >= 50, 1),
                else_=0
            )
            
            # Calculate volunteer hours
            volunteer_hours = db.session.query(func.coalesce(func.sum(attendance_table.c.hours), 0))\
                .select_from(attendance_table)\
                .join(Event, Event.event_id == attendance_table.c.event_id)\
                .where(attendance_table.c.profile_id == cls.profile_id)\
                .where(Event.organizer_id == org)\
                .where(Event.semester == current_semester)\
                .where(Event.meeting_type == MeetingType.VOLUNTEER)\
                .scalar_subquery()
            
            # Calculate volunteer points
            volunteer_points = case(
                (volunteer_hours >= 9, 4),
                (volunteer_hours >= 6, 3),
                (volunteer_hours >= 3, 2),
                (volunteer_hours >= 1, 1),
                else_=0
            )
            
            # Calculate mentorship meetings
            mentorship_meetings = db.session.query(func.count(Event.event_id))\
                .select_from(Event)\
                .join(attendance_table, Event.event_id == attendance_table.c.event_id)\
                .where(attendance_table.c.profile_id == cls.profile_id)\
                .where(Event.organizer_id == org)\
                .where(Event.semester == current_semester)\
                .where(Event.meeting_type == MeetingType.MENTORSHIP)\
                .scalar_subquery()
            
            mentorship_points = case(
                ((mentorship_meetings > 0) & (3 + mentorship_meetings <= 9), 3 + mentorship_meetings),
                ((mentorship_meetings > 0) & (3 + mentorship_meetings > 9), 9),
                else_=0
            )
            
            # Get bonus points
            bonus_points = cls.bonus_points_sql(org)
            
            # Calculate total points
            total_points = general_meeting_points + volunteer_points + mentorship_points + bonus_points
            
            return case(
                (total_points >= 16, "active"),
                else_="inactive"
            )
        
        else:
            # Default case for unknown organizations
            return "'unknown'"
    
    @hybrid_method
    def bonus_points(self, org: int, semester_only: bool = True):
        if semester_only:
            current_semester = (datetime.now(timezone.utc).year * 10) + (0 if datetime.now(timezone.utc).month <= 7 else 5)
            return sum(
                b.point_value for b in self.bonuses 
                if b.organization_id == org and 
                   ((b.created_at.year * 10) + (0 if b.created_at.month <= 7 else 5)) == current_semester
            )
        else:
            return sum(b.point_value for b in self.bonuses if b.organization_id == org)
    
    
    @bonus_points.expression
    @classmethod
    def bonus_points_sql(cls, org: int, semester_only: bool = True):
        if semester_only:
            # Get current semester
            current_semester = (datetime.now(timezone.utc).year * 10) + ((datetime.now(timezone.utc).month // 7) * 5)
            
            # Query that selects sum of bonus points for the given organization in the current semester
            return db.session.query(func.coalesce(func.sum(BonusPoints.point_value), 0))\
                .where(BonusPoints.recipient_id == cls.profile_id)\
                .where(BonusPoints.organization_id == org)\
                .where(func.strftime('%Y', BonusPoints.created_at) * 10 + 
                       cast(func.strftime('%m', BonusPoints.created_at) / 7, Integer) * 5 == current_semester)\
                .scalar_subquery()
        else:
            # Query that selects sum of all bonus points for the given organization
            return db.session.query(func.coalesce(func.sum(BonusPoints.point_value), 0))\
                .where(BonusPoints.recipient_id == cls.profile_id)\
                .where(BonusPoints.organization_id == org)\
                .scalar_subquery()
    
    @hybrid_method
    def event_points(self, org: int):
        return sum(e.point_value for e in self.attendance if e.organizer_id == org)
    
    @event_points.expression
    @classmethod
    def event_points_sql(cls, org: int):
        return db.session.query(func.coalesce(func.sum(Event.point_value), 0))\
            .select_from(Event)\
            .join(attendance_table, attendance_table.c.profile_id == cls.profile_id)\
            .where(Event.event_id == attendance_table.c.event_id)\
            .where(Event.organizer_id == org)\
            .scalar_subquery()
    
    @hybrid_method
    def points(self, org: int):
        return self.event_points(org) + self.bonus_points(org)
    
    
    @hybrid_method
    def semesters(self, org: int):
        return len(set(
            (event.start_time.month // 7, event.start_time.year) for event in self.attendance if event.organizer_id == org
        ))
        
    @semesters.expression
    @classmethod
    def semesters_sql(cls, org: int):
        return db.session.query(func.count()).select_from(
            db.session.query(cast(func.strftime('%m', Event.start_time) / 7, Integer), func.strftime('%Y', Event.start_time))\
                .correlate(cls)\
                .select_from(Event)\
                .join(attendance_table, attendance_table.c.event_id == Event.event_id)\
                .where(attendance_table.c.profile_id == cls.profile_id)\
                .where(Event.organizer_id == org)\
                .distinct().subquery()
        ).scalar_subquery()

    def membership_semesters(self, org: int):
        total = 0
        for semester in set(((event.start_time.month // 7 * 5) + event.start_time.year * 10) for event in self.attendance if event.organizer_id == org):
            total += 1 if self.membership(org, semester) else 0
        return total

    # profile_id = db.Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    # rit_id = db.Column(Text, nullable=False)
    # last_name = db.Column(String(50), nullable=False)
    # first_name = db.Column(String(50), nullable=False)
    # email = db.Column(Text, nullable=False)
    # graduation_year = db.Column(SmallInteger)
    # degree = db.Column(Text)
    # pronouns = db.Column(String(10))
    # avatar_path = db.Column(Text)
    # awards = relationship('ProfileAward', back_populates='profile')
    # administrators = relationship('Administrator', back_populates='profile')
    # attendance = relationship('Attendance', back_populates='profile')

    def serialize(self, org_id: Optional[int] = None) -> dict[str, Any]:
        base_profile_json = {
            "profile_id": self.profile_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
        
        if org_id is not None:
            base_profile_json['membership'] = self.membership(org_id)
            base_profile_json['semesters'] = self.semesters(org_id)
            base_profile_json["bonus_points"] = self.bonus_points(org_id)
            base_profile_json["attendance"] = [
                {
                    "event_id": event.event_id,
                    "name": event.name,
                    "description": event.description,
                    "meeting_type": event.meeting_type.value,
                    "point_value": event.point_value,
                    "organizer_id": event.organizer_id,
                    "start_time": event.start_time.isoformat(),
                    "semester": event.semester,
                    "hours": db.session.query(attendance_table.c.hours).where(attendance_table.c.profile_id == self.profile_id).where(attendance_table.c.event_id == event.event_id).first()[0]
                    
                } for event in self.attendance if event.organizer_id == org_id
            ]
        else:
            base_profile_json["attendance"] = [
                {
                    "event_id": event.event_id,
                    "name": event.name,
                    "description": event.description,
                    "meeting_type": event.meeting_type.value,
                    "point_value": event.point_value,
                    "start_time": event.start_time.isoformat(),
                    "organizer_id": event.organizer_id,
                    "semester": event.semester,
                    "hours": db.session.query(attendance_table.c.hours).where(attendance_table.c.profile_id == self.profile_id).where(attendance_table.c.event_id == event.event_id).first()[0]
                    
                } for event in self.attendance
            ]

        if self.rit_id is None:
            return {
                "incomplete": True,
                "profile": base_profile_json
            }
        else:
            base_profile_json.update({
                "rit_id": self.rit_id,
                "graduation_year": self.graduation_year,
                "degree": self.degree,
                "pronouns": self.pronouns,
                "avatar_path": self.avatar_path,
                
                "awards": [
                    {
                        "award_id": award.award_id,
                        "name": award.name,
                        "description": award.description,
                        "icon_path": award.icon_path,
                        "prize": award.prize,
                        "award_date": db.session.query(ProfileAward.award_date).where(ProfileAward.profile_id == self.profile_id).where(ProfileAward.award_id == award.award_id).first()[0].isoformat()
                    } for award in self.awards if org_id is None or award.organization_id == org_id
                ],
                
                "positions": [{
                    "organization_id": position.organization_id,
                    "role": position.role.value
                } for position in self.positions]
            })
            return {
                "incomplete": False,
               "profile": base_profile_json
            }

class BonusPoints(db.Model):
    __tablename__ = "BonusPoints"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    point_value: Mapped[int]
    recipient_id: Mapped[int] = mapped_column(ForeignKey("Profile.profile_id"))
    recipient: Mapped["Profile"] = relationship("Profile", foreign_keys=[recipient_id], back_populates="bonuses")
    giver_id: Mapped[int] = mapped_column(ForeignKey("Profile.profile_id"))
    giver: Mapped["Profile"] = relationship("Profile", foreign_keys=[giver_id], back_populates="grants")
    reason: Mapped[str]
    organization_id: Mapped[int] = mapped_column(ForeignKey("Organizer.organization_id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

class Award(db.Model):
    __tablename__ = 'Award'

    award_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    name: Mapped[str]
    description: Mapped[str]
    icon_path: Mapped[str]
    prize: Mapped[str]
    organization_id: Mapped[int] = mapped_column(ForeignKey("Organizer.organization_id"))
    active_semester_requirements: Mapped[int]

    # conditions: Mapped[list["AwardCondition"]] = relationship(back_populates="award")
    recipients: Mapped[list["Profile"]] = relationship(secondary="ProfileAward", back_populates="awards")

    # award_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # name = db.Column(String(50), nullable=False)
    # description = db.Column(Text, nullable=False)
    # icon_path = db.Column(String(50))
    # prize = db.Column(Text)
    # conditions = relationship('AwardCondition', back_populates='award')
    # profile_awards = relationship('ProfileAward', back_populates='award')

# class AwardCondition(db.Model):
#     __tablename__ = 'AwardCondition'

#     condition_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
#     name: Mapped[str]
#     point_requirement: Mapped[Optional[int]]
#     meeting_requirement: Mapped[Optional[int]]
#     # meeting_type: Mapped[list[MeetingType]]
#     check_time: Mapped[str]
#     award: Mapped["Award"] = relationship(back_populates="conditions")
#     award_id: Mapped[int] = mapped_column(ForeignKey("Award.award_id"))

    # condition_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # name = db.Column(Text, nullable=False)
    # point_requirement = db.Column(Integer)
    # meeting_requirement = db.Column(Integer)
    # meeting_type = db.Column(ARRAY(String))
    # check_time = db.Column(Text)
    # award_id = db.Column(Integer, ForeignKey('Award.award_id'))
    # award = relationship('Award', back_populates='conditions')

class ProfileAward(db.Model):
    __tablename__ = 'ProfileAward'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    profile_id: Mapped[int] = mapped_column(ForeignKey("Profile.profile_id"))
    award_id: Mapped[int] = mapped_column(ForeignKey("Award.award_id"))
    award_date: Mapped[datetime]
    # id = db.Column(Integer, primary_key=True, autoincrement=True)
    # profile_id = db.Column(Integer, ForeignKey('Profile.profile_id'), nullable=False)
    # award_id = db.Column(Integer, ForeignKey('Award.award_id'), nullable=False)
    # date_received = db.Column(DateTime, nullable=False)
    # profile = relationship('Profile', back_populates='awards')
    # award = relationship('Award', back_populates='profile_awards')

class Administrator(db.Model):
    __tablename__ = 'Administrator'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    role: Mapped[RoleType]
    profile: Mapped["Profile"] = relationship("Profile", back_populates="positions")
    profile_id: Mapped[int] = mapped_column(ForeignKey("Profile.profile_id"))
    organization: Mapped["Organizer"] = relationship("Organizer", back_populates="administrators")
    organization_id: Mapped[int] = mapped_column(ForeignKey("Organizer.organization_id"))
    # id = db.Column(Integer, primary_key=True, autoincrement=True)
    # profile_id = db.Column(Integer, ForeignKey('Profile.profile_id'), nullable=False)
    # role = db.Column(Enum('roleType'), nullable=False)
    # profile = relationship('Profile', back_populates='administrator')

class Organizer(db.Model):
    __tablename__ = 'Organizer'

    organization_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    name: Mapped[str]
    email: Mapped[str]
    events: Mapped[list["Event"]] = relationship(back_populates="organizer")
    administrators: Mapped[list["Administrator"]] = relationship("Administrator", foreign_keys="[Administrator.organization_id]", back_populates="organization")
   
    # organization_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # name = db.Column(String(50), nullable=False)
    # email = db.Column(Text, nullable=False)
    # events = relationship('Event', back_populates='organizer')

class Event(db.Model):
    __tablename__ = 'Event'

    event_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    meeting_type: Mapped[MeetingType]
    name: Mapped[str]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    location: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    point_value: Mapped[int] = mapped_column(default=0)
    organizer: Mapped["Organizer"] = relationship(back_populates="events")
    organizer_id: Mapped[int] = mapped_column(ForeignKey("Organizer.organization_id"))
    attendants: Mapped[list["Profile"]] = relationship(secondary=attendance_table, back_populates="attendance")
    # event_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # campus_group_id = db.Column(Integer, nullable=False)
    # meeting_type= db.Column(Enum(MeetingType), nullable=False)
    # name = db.Column(Text, nullable=False)
    # start_time = db.Column(DateTime, nullable=False)
    # end_time = db.Column(DateTime, nullable=False)
    # description = db.Column(Text, nullable=False)
    # point_value = db.Column(Integer, default=0)
    # organizer_id = db.Column(Integer, ForeignKey('Organizer.organization_id'))
    # organizer = relationship('Organizer', back_populates='events')
    # attendance = relationship('Attendance', back_populates='event')

    def get_hours(self, profile_id: int) -> int:
        row = db.session.query(attendance_table.c.hours)\
        .filter(attendance_table.c.event_id == self.event_id)\
        .filter(attendance_table.c.profile_id == profile_id)\
        .first()

        if row is None:
            return 0
        else:
            return row[0]

    @hybrid_property
    def semester(self):
        return (self.start_time.year * 10) + ((self.start_time.month // 7) * 5)

    @semester.inplace.expression
    def semester_sql(cls):
        return (func.strftime('%Y', Event.start_time) * 10) + (cast(func.strftime('%m', Event.start_time) / 7, Integer) * 5)


class Token(db.Model):
    __tablename__ = 'Token'

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("Organizer.organization_id"))

    token: Mapped[str]
    refresh_token: Mapped[str]
    token_uri: Mapped[str]
    client_id: Mapped[str]
    client_secret: Mapped[str]
    expirey: Mapped[datetime]

    email: Mapped[str]

# class Attendance(db.Model):
#     __tablename__ = 'Attendance'

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
#     profile_id: Mapped[int] = relationship(ForeignKey("Profile.profile_id"))
#     event_id: Mapped[int] = relationship(ForeignKey("Event.event_id"))
    
    # id = db.Column(Integer, primary_key=True, autoincrement=True)
    # profile_id = db.Column(Integer, ForeignKey('Profile.profile_id'), nullable=False)
    # event_id = db.Column(Integer, ForeignKey('Event.event_id'), nullable=False)
    # profile = relationship('Profile', back_populates='attendance')
    # event = relationship('Event', back_populates='attendance')
    
    
def db_testing_setup():
    import json
    import random
    from datetime import datetime
    
    users = []
    events= []
    
    WiC = Organizer(
        name = "Women in Computing",
        email = "wic@rit.edu"
    )
    
    COMS = Organizer(
        name = "Computing Organization for Multicultural Students",
        email = "coms@rit.edu"
    )

    wic_award = Award(
        organization_id = Organizations.WIC,
        name = "being super cool award",
        description = "For gamers only",
        icon_path = "../static/images/award.webp",
        prize = "6 Dining Dollars",
        active_semester_requirements = 2
    )

    coms_award = Award(
        organization_id = Organizations.COMS,
        name = "being super cool award",
        description = "For gamers only",
        icon_path = "../static/images/award.webp",
        prize = "6 Dining Dollars",
        active_semester_requirements = 1
    )
    
    with open("testing_data/users.json") as f:
        user_data = json.load(f)
        
    for user in user_data:
        users.append(
            Profile(**user)
        )

    for i in range(20):
        for meeting_type in (
                MeetingType.GENERAL,
                MeetingType.COMMITTEE,
                MeetingType.MENTORSHIP,
                MeetingType.SOCIAL,
                MeetingType.VOLUNTEER
            ):
            event = Event(
                meeting_type = meeting_type,
                name = f"Active User Event {i}",
                start_time = datetime.now(timezone.utc),
                end_time = datetime.now(timezone.utc),
                organizer_id = Organizations.WIC
            )

            for user in users[:50]:
                user.attendance.append(event)

        events.append(event)

    active_users = users[:50]

    with open("testing_data/events.json") as f:
        event_data = json.load(f)
        
    for event in event_data:
        events.append(Event(
            **event,
            organizer=random.choice([WiC, COMS])
        ))
        events[-1].meeting_type = random.choice([
            MeetingType.GENERAL,
            MeetingType.VOLUNTEER,
            MeetingType.SOCIAL,
            MeetingType.MENTORSHIP,
            MeetingType.COMMITTEE
        ])
        events[-1].start_time = datetime.strptime(events[-1].start_time, "%Y-%m-%d %H:%M:%S")
        events[-1].start_time = events[-1].start_time.replace(year=datetime.now().year, month=datetime.now().month - 1)
        events[-1].end_time = datetime.strptime(events[-1].end_time, "%Y-%m-%d %H:%M:%S")
        events[-1].end_time = events[-1].end_time.replace(year=datetime.now().year, month=datetime.now().month - 1)

    developer_profiles_data = [
        {
          "rit_id": "bp3940",
          "first_name": "Blanka",
          "last_name": "Peller",
          "email": "bp3940@rit.edu"
        },
        {
          "rit_id": "njz8626",
          "first_name": "Nathan",
          "last_name": "Zilora",
          "email": "njz8626@rit.edu"
        },
        {
            "rit_id": "whb3080",
            "first_name": "Wyatt",
            "last_name": "IDK",
            "email": "whb3080@rit.edu"
        },
        {
          "rit_id": "rwc5591",
          "first_name": "Reg",
          "last_name": "Chuhi",
          "email": "rwc5591@rit.edu"   
        },
        {
          "rit_id": "dks7712",
          "first_name": "Dylan",
          "last_name": "Sandberg",
          "email": "dks7712@rit.edu"
        },
        {
        "rit_id": "vah7365",
        "first_name": "Vivian",
        "last_name": "Hernandez",
        "email": "vah7365@rit.edu"
        }
    ]

    developer_profiles = [Profile(**data) for data in developer_profiles_data]

    will_smith = Profile(
        rit_id = "wls1234",
        first_name = "Will",
        last_name = "Smith",
        email = "wls1234@rit.edu",
        graduation_year = 2025,
        degree = "Acting",
        pronouns = "He/Him"
    )

    db.session.add_all([
        *users, *events, WiC, COMS, will_smith, *developer_profiles, wic_award, coms_award
    ])
    db.session.commit()

    for event in events:
        for user in random.choices(users, k=random.randint(0, 120)):
            create_attendance(user.email, event.event_id, user.first_name, user.last_name, random.randint(1,8))

    for event in db.session.query(Event).all():
        create_attendance(will_smith.email, event.event_id, will_smith.first_name, will_smith.last_name, random.randint(1, 8))
        for user in developer_profiles:
                create_attendance(user.email, event.event_id, user.first_name, user.last_name, random.randint(1, 8))

    assign_awards = []

    users.append(will_smith)

    for semester in range(20220, 20250, 5):
        for user in random.choices(users, k=random.randint(100, len(users) // 2)):
            assign_awards.append(
                ProfileAward(
                    profile_id = user.profile_id,
                    award_id = wic_award.award_id,
                    award_date = datetime(year = semester // 10, month = 10 if semester % 5 else 2, day = 10)
                )
            )
            assign_awards.append(
                ProfileAward(
                    profile_id = user.profile_id,
                    award_id = coms_award.award_id,
                    award_date = datetime(year = semester // 10, month = 10 if semester % 5 else 2, day = 10)
                )
            )

    db.session.add_all(assign_awards)

    make_admin(will_smith.profile_id, Organizations.WIC, RoleType.ADMIN)
    make_admin(will_smith.profile_id, Organizations.COMS, RoleType.ADMIN)

    for user in developer_profiles:
        make_admin(user.profile_id, Organizations.WIC, RoleType.ADMIN)
        make_admin(user.profile_id, Organizations.COMS, RoleType.ADMIN)

    db.session.commit()

    for user in active_users:
        print(user.profile_id, user.first_name, user.last_name)

def make_admin(user: int, org: int, role: RoleType):
    admin = Administrator(
        profile_id = user,
        organization_id = org,
        role = role
    )

    db.session.add(admin)
    return admin

def create_attendance(email: str, event_id: int, first_name: str = None, last_name: str = None, hours = 0):
    """
    Creates an attendance object that has NOT been committed yet.
    """
    user = Profile.query.where(Profile.email == email).first()
    event = Event.query.get(event_id)

    if event is None:
        raise ValueError("Unable to find event")
    
    if user is None:
        user = Profile(email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
    
    if event not in user.attendance:
        with db.engine.connect() as conn:
            conn.execute(
                attendance_table.insert().values(
                    event_id = event_id,
                    profile_id = user.profile_id,
                    hours = hours
                ).compile()
            )
            conn.commit()
        
    
    return user

def create_bonus(point_value: int, recipient_id: int, giver_id: int, reason: str, org: int):
    grant = BonusPoints(
        point_value = point_value,
        recipient_id = recipient_id,
        giver_id = giver_id,
        reason = reason,
        organization_id = org
    )
    db.session.add(grant)
    return grant

def commit(*objects: Base):
    if objects:
        db.session.add_all(objects)
    db.session.commit()
