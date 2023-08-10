from datetime import datetime, timedelta
from operator import and_

from flask_restful import marshal, fields

from application.database import db_session
from application.models import Booking, Show, Review, Theatre, User


def show_stat(id):
    """

    :param id:
    :return: last fifteen days rating and seats
    """
    rating_all = []
    seats_all = []

    # // number of tickets brought
    for x in range(0, 15):  # loop fifteen days
        seats_count = 0
        rating_sum, rating_c = 0, 0
        end = datetime.utcnow() - timedelta(days=x)
        start = end - timedelta(days=1)
        seats = db_session.query(Booking.seats).join(Show, Booking.show_name == Show.name).where(Show.id == id).filter(
            and_(end > Booking.timestamp, Booking.timestamp > start)).all()
        # take sum of seats
        seats = marshal(seats, {'seats': fields.String})
        for p in seats:
            for y in p['seats'].split(','):
                if y != '':
                    seats_count += 1

        ratings = db_session.query(Review.rating).where(Review.show_id == id).filter(
            and_(end > Review.timestamp, Review.timestamp > start)).all()
        # take mean of rating
        ratings = marshal(ratings, {'rating': fields.Integer})
        for p in ratings:
            print(p['rating'])
            if p['rating'] is not None:
                rating_sum += p['rating']
                rating_c += 1
        print(rating_sum, rating_c)
        rating_all.append(rating_sum / rating_c if rating_c != 0 else 0)

        seats_all.append(seats_count)

    return [rating_all, seats_all]


def t_revenue_collected(tid):
    result = []
    for x in range(1, 16):
        end = datetime.utcnow() - timedelta(days=x)
        start = end - timedelta(days=1)
        rev = (db_session.query(Booking.total_price).join(Theatre, Booking.theatre_name == Theatre.name)
               .where(Theatre.id == tid).filter(
            and_(end > Booking.timestamp, Booking.timestamp > start)).all())
        rev = marshal(rev, {'total_price': fields.Float})
        rev = sum([x['total_price'] for x in rev])
        result.append(rev)

    return result


def t_ticket_sold(tid):
    result = []
    for x in range(1, 16):
        seats_count = 0
        end = datetime.utcnow() - timedelta(days=x)
        start = end - timedelta(days=1)
        rev = (db_session.query(Booking.seats).join(Theatre, Booking.theatre_name == Theatre.name)
               .where(Theatre.id == tid).filter(
            and_(end > Booking.timestamp, Booking.timestamp > start)).all())
        seats = marshal(rev, {'seats': fields.String})
        for p in seats:
            for y in p['seats'].split(','):
                if y != '':
                    seats_count += 1
        result.append(seats_count)
    return result


def t_rating(tid):
    rating_all = []
    for x in range(1, 16):
        rating_sum, rating_c = 0, 0
        end = datetime.utcnow() - timedelta(days=x)
        start = end - timedelta(days=1)
        ratings = db_session.query(Review.rating).where(Review.theatre_id == id).filter(
            and_(end > Review.timestamp, Review.timestamp > start)).all()
        # take mean of rating
        ratings = marshal(ratings, {'rating': fields.Integer})
        for p in ratings:
            print(p['rating'])
            if p['rating'] is not None:
                rating_sum += p['rating']
                rating_c += 1
        rating_all.append(rating_sum / rating_c if rating_c != 0 else 0)


# def top_charts():
#     theatre= db_session.query(Theatre)


def monthly_er(email):
    uid = db_session.query(User.id).where(User.email == email).first()[0].__str__()
    books = marshal(
        db_session.query(Booking.total_price, Booking.date, Booking.start, Booking.end, Show.name, Show.image_url,
                         Show.director).join(Show, Booking.show_name == Show.name).where(
            Booking.user_id == uid).all(), {'image_url': fields.String,
                                            'total_price': fields.Float,
                                            'date': fields.String,
                                            'start': fields.String,
                                            'end': fields.String,
                                            'name': fields.String,
                                            'director': fields.String,
                                            })
    reviews = marshal(
        db_session.query(Review.rating, Review.review, Show.name).join(Show, Show.id == Review.show_id).where(
            Review.user_id == uid).order_by(Review.show_id, Review.theatre_id).all(),
        {'rating': fields.Integer,
         'review': fields.String,
         'name': fields.String,
         })
    # ToDo: Add recommendations
    return [books, reviews]
