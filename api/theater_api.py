from flask_restful import Resource, reqparse, abort, marshal_with, fields
from sqlalchemy.exc import NoResultFound

from application.database import db_session
from application.models import Theatre


def abort_if_theatre_doesnt_exist(tid):
    try:
        Theatre.query.filter_by(id=tid).one()
    except NoResultFound as e:
        abort(404, message="Theatre with ID: {} doesn't exist".format(tid))

parser = reqparse.RequestParser()  # for GET, DELETE requests
parser.add_argument('id', required=True, type=int, location='args')

parser2 = reqparse.RequestParser()  # for POST, PUT  requests
parser2.add_argument('id', required=False, type=int)
parser2.add_argument('name', required=True, type=str)
parser2.add_argument('place', required=False, type=str)
parser2.add_argument('capacity', required=False, type=str)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'place': fields.String,
    'capacity': fields.String,
}


class TheatresAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # // get all Theatres
        # // return all Theatres
        tid = parser.parse_args()['id']
        abort_if_theatre_doesnt_exist(tid)
        if tid:
            stmt = Theatre.query.filter_by(id=tid)
            return stmt.one()

    @marshal_with(resource_fields)
    def post(self):
        # // add theatre to database
        # // return theatre id
        args = parser2.parse_args()
        theatre = Theatre(
            name=args['name'],
            place=args['place'],
            capacity=args['capacity'])
        db_session.add(theatre)
        db_session.commit()
        return theatre

    def delete(self):
        # // delete theatre from database
        # // return theatre id
        tid = parser.parse_args()['id']
        abort_if_theatre_doesnt_exist(tid)
        stmt = Theatre.query.filter_by(id=tid).one()
        db_session.delete(stmt)
        db_session.commit()
        return "Operation Successful", 200

    @marshal_with(resource_fields)
    def put(self):
        # // update theatre in database
        # // return theatre id
        args = parser2.parse_args()
        abort_if_theatre_doesnt_exist(args['id'])
        theatre = db_session.query(Theatre).filter_by(id=args['id'])
        theatre.update(args)
        db_session.commit()
        return theatre.one()
