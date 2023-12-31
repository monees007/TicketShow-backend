from flask_restful import Resource, reqparse, abort, marshal_with, fields
from flask_security import current_user
from sqlalchemy.exc import NoResultFound

from application.database import db_session
from application.models import Booking


def abort_if_booking_doesnt_exist(bid):
    try:
        Booking.query.filter_by(id=bid).one()
    except NoResultFound as e:
        abort(404, message="Booking with ID: {} doesn't exist".format(bid))


parser = reqparse.RequestParser()  # for GET, DELETE requests
parser.add_argument('id', required=True, type=int, location='args')

parser2 = reqparse.RequestParser()  # for POST, PUT  requests
parser2.add_argument('id', required=False, type=int)
parser2.add_argument('running_id', required=True, type=int)
parser2.add_argument('seats', required=True, type=str)
parser2.add_argument('total_price', required=True, type=str)
parser2.add_argument('theatre_name', required=True, type=str)
parser2.add_argument('theatre_place', required=True, type=str)
parser2.add_argument('show_name', required=True, type=str)
parser2.add_argument('language', required=True, type=str)
parser2.add_argument('format', required=True, type=str)
parser2.add_argument('date', required=True, type=str)
parser2.add_argument('start', required=True, type=str)
parser2.add_argument('end', required=True, type=str)

resource_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'running_id': fields.Integer,
    'seats': fields.String,
    'theatre_name': fields.String,
    'theatre_place': fields.String,
    'show_name': fields.String,
    'language': fields.String,
    'format': fields.String,
    'date': fields.String,
    'start': fields.String,
    'end': fields.String,
    'total_price': fields.String
}


class BookingsAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # // get all bookings
        # // return all bookings
        bid = parser.parse_args()['id']

        if bid < 0:
            stmt = Booking.query.filter_by(user_id=current_user.id)
            return stmt.all()
        else:
            stmt = Booking.query.filter_by(id=bid)
            return stmt.one()

    @marshal_with(resource_fields)
    def post(self):
        # // add booking to database
        # // return booking id
        args = parser2.parse_args()
        booking = Booking(
            user_id=current_user.id,
            running_id=args['running_id'],
            seats=args['seats'],
            theatre_name=args['theatre_name'],
            theatre_place=args['theatre_place'],
            show_name=args['show_name'],
            language=args['language'],
            format=args['format'],
            date=args['date'],
            start=args['start'],
            end=args['end'],
            total_price=args['total_price'])
        db_session.add(booking)
        db_session.commit()
        return booking


def delete(self):
    # // delete booking from database
    # // return booking id
    bid = parser.parse_args()['id']
    abort_if_booking_doesnt_exist(bid)
    stmt = Booking.query.filter_by(id=bid).one()
    # stmt.delete()
    db_session.delete(stmt)
    db_session.commit()
    return "Operation Successful", 200


@marshal_with(resource_fields)
def put(self):
    # // update booking in database
    # // return booking id
    args = parser2.parse_args()
    abort_if_booking_doesnt_exist(args['id'])
    booking = db_session.query(Booking).filter_by(id=args['id'])
    booking.update(args)
    db_session.commit()
    return booking.one()
