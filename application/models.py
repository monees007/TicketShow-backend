from flask_security import UserMixin, RoleMixin
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, UnicodeText, Float, func
from sqlalchemy.orm import relationship, backref

from application.database import Base


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(UnicodeText)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    set_uniquifier = Column(String(255), unique=True, nullable=True)
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Theatre(Base):
    __tablename__ = "theatre"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    place = Column(String(255), nullable=False)
    capacity = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("user.id"))
    rating = Column(Integer)
    city = Column(String(255))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Show(Base):
    __tablename__ = "show"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    rating = Column(Integer)
    year = Column(Integer)
    director = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    duration = Column(Integer)
    image_url = Column(String(255), nullable=True)
    image_sqr = Column(String(255), nullable=True)
    tags = Column(String(255), nullable=True)
    ticket_price = Column(Float())
    format = Column(String(255), nullable=False)
    language = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Running(Base):
    __tablename__ = "running"
    id = Column(Integer, primary_key=True)
    theatre_id = Column(Integer, ForeignKey("theatre.id"))
    show_id = Column(Integer, ForeignKey("show.id"))
    date = Column(DateTime(), server_default=func.now())

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    running_id = Column(Integer, ForeignKey("running.id"))
    seats = Column(String(255))
    total_price = Column(Float())

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    show_id = Column(Integer, ForeignKey("show.id"))
    theatre_id = Column(Integer, ForeignKey("theatre.id"))
    rating = Column(Integer)
    review = Column(String(255))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class UserReview(Base):
    __tablename__ = "user_review"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    review_id = Column(Integer, ForeignKey("review.id"))
    like = Column(Boolean)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
