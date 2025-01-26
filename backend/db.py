from enum import Enum as EnumClass

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, Integer, String, Text, SmallInteger, Enum, ARRAY
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)


class MeetingType(EnumClass):
    GENERAL = 0

class Profile(db.Model):
    __tablename__ = 'Profile'
    profile_id = db.Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    rit_id = db.Column(Text, nullable=False)
    last_name = db.Column(String(50), nullable=False)
    first_name = db.Column(String(50), nullable=False)
    email = db.Column(Text, nullable=False)
    graduation_year = db.Column(SmallInteger)
    degree = db.Column(Text)
    pronouns = db.Column(String(10))
    avatar_path = db.Column(Text)
    awards = relationship('ProfileAward', back_populates='profile')
    administrators = relationship('Administrator', back_populates='profile')
    attendance = relationship('Attendance', back_populates='profile')

class Award(db.Model):
    __tablename__ = 'Award'
    award_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(String(50), nullable=False)
    description = db.Column(Text, nullable=False)
    icon_path = db.Column(String(50))
    prize = db.Column(Text)
    conditions = relationship('AwardCondition', back_populates='award')
    profile_awards = relationship('ProfileAward', back_populates='award')

# class AwardCondition(db.Model):
#     __tablename__ = 'AwardCondition'
#     condition_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
#     name = db.Column(Text, nullable=False)
#     point_requirement = db.Column(Integer)
#     meeting_requirement = db.Column(Integer)
#     meeting_type = db.Column(ARRAY(String))
#     check_time = db.Column(Text)
#     award_id = db.Column(Integer, ForeignKey('Award.award_id'))
#     award = relationship('Award', back_populates='conditions')

# class ProfileAward(db.Model):
#     __tablename__ = 'ProfileAward'
#     id = db.Column(Integer, primary_key=True, autoincrement=True)
#     profile_id = db.Column(Integer, ForeignKey('Profile.profile_id'), nullable=False)
#     award_id = db.Column(Integer, ForeignKey('Award.award_id'), nullable=False)
#     date_received = db.Column(DateTime, nullable=False)
#     profile = relationship('Profile', back_populates='awards')
#     award = relationship('Award', back_populates='profile_awards')

class Administrator(db.Model):
    __tablename__ = 'Administrators'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(Integer, ForeignKey('Profile.profile_id'), nullable=False)
    role = db.Column(Enum('roleType'), nullable=False)
    profile = relationship('Profile', back_populates='administrators')

class Organizer(db.Model):
    __tablename__ = 'Organizer'
    organization_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(String(50), nullable=False)
    email = db.Column(Text, nullable=False)
    events = relationship('Event', back_populates='organizer')

class Event(db.Model):
    __tablename__ = 'Event'
    event_id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    campus_group_id = db.Column(Integer, nullable=False)
    meeting_type= db.Column(Enum(MeetingType), nullable=False)
    name = db.Column(Text, nullable=False)
    start_time = db.Column(DateTime, nullable=False)
    end_time = db.Column(DateTime, nullable=False)
    description = db.Column(Text, nullable=False)
    point_value = db.Column(Integer, default=0)
    organizer_id = db.Column(Integer, ForeignKey('Organizer.organization_id'))
    organizer = relationship('Organizer', back_populates='events')
    attendance = relationship('Attendance', back_populates='event')

class Attendance(db.Model):
    __tablename__ = 'Attendance'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(Integer, ForeignKey('Profile.profile_id'), nullable=False)
    event_id = db.Column(Integer, ForeignKey('Event.event_id'), nullable=False)
    profile = relationship('Profile', back_populates='attendance')
    event = relationship('Event', back_populates='attendance')
