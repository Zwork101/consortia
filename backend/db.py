from datetime import datetime
from enum import Enum as EnumClass
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String, Text, SmallInteger, Enum, ARRAY

db = SQLAlchemy()


class MeetingType(EnumClass):
    GENERAL = "GENERAL"


class RoleType(EnumClass):
    ADMIN = "ADMIN"
    PLANNER = "PLANNER"

class Profile(db.Model):
    __tablename__ = 'Profile'

    profile_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    rit_id: Mapped[int]
    last_name: Mapped[str]
    first_name: Mapped[str]
    email: Mapped[str]
    graduation_year: Mapped[int]
    degree: Mapped[str]
    pronouns: Mapped[str]
    avatar_path: Mapped[str]

    attendance: Mapped[list["Event"]] = relationship(secondary="Attendance", back_populates="attendants")
    awards: Mapped[list["Award"]] = relationship(secondary="ProfileAward", back_populates="recipients")
    administrator: Mapped["Administrator"] = relationship(back_populates="profile")

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

class Award(db.Model):
    __tablename__ = 'Award'

    award_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    name: Mapped[str]
    description: Mapped[str]
    icon_path: Mapped[str]
    prize: Mapped[str]

    conditions: Mapped[list["AwardCondition"]] = relationship(back_populates="award")
    recipients: Mapped[list["Profile"]] = relationship(secondary="ProfileAward", back_populates="awards")

    # award_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # name = db.Column(String(50), nullable=False)
    # description = db.Column(Text, nullable=False)
    # icon_path = db.Column(String(50))
    # prize = db.Column(Text)
    # conditions = relationship('AwardCondition', back_populates='award')
    # profile_awards = relationship('ProfileAward', back_populates='award')

class AwardCondition(db.Model):
    __tablename__ = 'AwardCondition'

    condition_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    name: Mapped[str]
    point_requirement: Mapped[Optional[int]]
    meeting_requirement: Mapped[Optional[int]]
    # meeting_type: Mapped[list[MeetingType]]
    check_time: Mapped[str]
    award: Mapped["Award"] = relationship(back_populates="conditions")

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
    profile: Mapped["Profile"] = relationship("Profile", back_populates="administrator")
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
    description: Mapped[str]
    point_value: Mapped[int]
    organizer: Mapped["Organizer"] = relationship(back_populates="events")
    attendants: Mapped["Profile"] = relationship(secondary="Attendance", back_populates="attendance")
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

class Attendance(db.Model):
    __tablename__ = 'Attendance'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    profile_id: Mapped[int] = relationship(ForeignKey("Profile.profile_id"))
    event_id: Mapped[int] = relationship(ForeignKey("Event.event_id"))
    # id = db.Column(Integer, primary_key=True, autoincrement=True)
    # profile_id = db.Column(Integer, ForeignKey('Profile.profile_id'), nullable=False)
    # event_id = db.Column(Integer, ForeignKey('Event.event_id'), nullable=False)
    # profile = relationship('Profile', back_populates='attendance')
    # event = relationship('Event', back_populates='attendance')
