from datetime import datetime, timedelta
from operator import and_

from flask_restful import marshal, fields

from application.database import db_session
from application.models import Booking, Show, Review, Theatre, User, Running

"""
## show
  -  no of ticket brought // one ticket = one seat 
  -  floating average rating
  -  total revenue collected
    
## theatre
  -  no of bookings per show
  -  total tickets per day 
  -  floating average rating
  -  revenue collected
"""


def show_stat(id):
    """

    :param id:
    :return: last fifteen days rating and seats
    """
    rating_all = []
    seats_all = []
    total_revenue = 0

    # // number of tickets brought
    for x in range(0, 15):  # loop fifteen days
        seats_count = 0
        rating_sum, rating_c = 0, 0
        end = datetime.utcnow() - timedelta(days=x)
        start = end - timedelta(days=1)
        seats = db_session.query(Booking.seats, Booking.total_price).join(Show, Booking.show_name == Show.name).where(
            Show.id == id).filter(and_(end > Booking.timestamp, Booking.timestamp > start)).all()
        # take sum of seats
        seats = marshal(seats, {'seats': fields.String, 'total_price': fields.Float})
        for p in seats:
            total_revenue += p['total_price']
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

    return [rating_all, seats_all, total_revenue]


def t_revenue(tid):
    # total and show wise revenue
    # for x in range(1, 16):
    #     end = datetime.utcnow() - timedelta(days=x)
    #     start = end - timedelta(days=1)
    rev = (db_session.query(Booking.show_name, Booking.total_price).join(Theatre,
                                                                         Booking.theatre_name == Theatre.name).where(
        Theatre.id == tid).group_by(Booking.show_name).all())
    rev = marshal(rev, {'total_price': fields.Float, 'show_name': fields.String})
    total_revenue = sum([x['total_price'] for x in rev])
    return [total_revenue, rev]


def t_ticket_sold(tid, days):
    result = []
    revenue = []
    label = []
    show = {}  # [show_name:{ seats: , revenue: }]
    for x in range(days + 1, 1, -1):
        seats_count = 0
        temp_revenue = 0

        end = datetime.utcnow() - timedelta(days=x)
        start = end - timedelta(days=1)
        rev = (db_session.query(Booking.seats, Booking.total_price, Running.show_name).join(Running,
                                                                                            Booking.running_id == Running.id).where(
            Running.theatre_id == tid).filter(and_(start < Booking.timestamp, Booking.timestamp < end)).all())
        for p in rev:
            if p[2] not in show:
                show[p[2]] = {'seats': 0, 'revenue': 0}
            show[p[2]]['revenue'] += p[1]
            temp_revenue += p[1]
            for y in p[0].split(','):
                if y != '':
                    show[p[2]]['seats'] += 1
                    seats_count += 1

        result.append(int(seats_count))
        revenue.append(int(temp_revenue))
        label.append(end.strftime("%d %b"))
    return result, revenue, label, show


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


def combine_rating(L):
    """
    take a list of rating and combines them
    :param L: List of rating
    :return: Integer
    """
    sum = 0
    for x in L:
        sum += int(x)
    return sum // len(L) if len(L) != 0 else 0


def monthly_erX(email):
    uid = db_session.query(User.id).where(User.email == email).first()[0].__str__()
    books = marshal(
        db_session.query(Booking.total_price, Booking.date, Booking.start, Booking.end, Show.name, Show.image_url,
                         Show.director).join(Show, Booking.show_name == Show.name).where(Booking.user_id == uid).all(),
        {'image_url': fields.String, 'total_price': fields.Float, 'date': fields.String, 'start': fields.String,
         'end': fields.String, 'name': fields.String, 'director': fields.String, })
    reviews = marshal(
        db_session.query(Review.rating, Review.review, Show.name).join(Show, Show.id == Review.show_id).where(
            Review.user_id == uid).order_by(Review.show_id, Review.theatre_id).all(),
        {'rating': fields.Integer, 'review': fields.String, 'name': fields.String, })
    # ToDo: Add recommendations
    return [books, reviews]


allowed_seat_code = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',
                     'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',
                     'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
                     'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']


def generate_fake_bookings():
    """
    Generate fake bookings for testing over the last 15 days
    :return:
    """
    from datetime import datetime, timedelta
    import random
    current_date = datetime.now().date()
    for i in range(15):
        date = current_date - timedelta(days=i)
        stmt = Running.query.all()
        for run in [x.as_dict() for x in stmt]:
            # iterating over each running
            for x in range(random.randint(1, 10)):
                booking = Booking(
                    user_id=3,
                    running_id=run['id'],
                    seats=",".join(random.sample(allowed_seat_code, 5)),
                    theatre_name='theatre_name',
                    theatre_place='theatre_place',
                    show_name='show_name',
                    language=run['language'],
                    format=run['format'],
                    date=date + timedelta(days=random.randint(1, 3)),
                    start=run['start'],
                    end=run['end'],
                    timestamp=date,
                    total_price=float(run['ticket_price']) * 5, )
                db_session.add(booking)
                db_session.commit()
    return 200, "Done"
