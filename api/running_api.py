from flask_restful import Resource, reqparse, abort, marshal_with, fields
from sqlalchemy.exc import NoResultFound

from api.show_api import abort_if_show_doesnt_exist
from api.theater_api import abort_if_theatre_doesnt_exist
from application.database import db_session
from application.models import Running


def abort_if_running_doesnt_exist(rid):
    try:
        Running.query.filter_by(id=rid).one()
    except NoResultFound as e:
        abort(404, "Running with ID: {} doesn't exist")


parser = reqparse.RequestParser()  # for GET, DELETE requests
parser.add_argument('id', required=False, type=int, location='args')
parser.add_argument('sid', required=False, type=int, location='args')

parser2 = reqparse.RequestParser()  # for POST, PUT  requests
parser2.add_argument('id', required=False, type=int)
parser2.add_argument('theatre_id', required=False, type=int)
parser2.add_argument('show_id', required=False, type=int)
parser2.add_argument('show_name', required=False, type=str)
parser2.add_argument('start', required=False, type=str)
parser2.add_argument('end', required=False, type=str)
parser2.add_argument('language', required=False, type=str)
parser2.add_argument('format', required=False, type=str)
parser2.add_argument('ticket_price', required=False, type=str)

parser3 = reqparse.RequestParser()  # for PATCH  requests
parser3.add_argument('id', required=True, type=int)
parser3.add_argument('occupied_seats', required=False, type=str)

resource_fields = {
    'id': fields.Integer,
    'theatre_id': fields.Integer,
    'show_id': fields.Integer,
    'show_name': fields.String,
    'start': fields.String,
    'end': fields.String,
    'language': fields.String,
    'format': fields.String,
    'ticket_price': fields.String,
    'occupied_seats': fields.String,

}


class RunningAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # // get all runnings
        # // return all runnings
        tid = parser.parse_args()['id']
        sid = parser.parse_args()['sid']
        abort_if_theatre_doesnt_exist(tid)
        if tid and sid:
            abort_if_show_doesnt_exist(sid)
            stmt = Running.query.filter_by(theatre_id=tid, show_id=sid).all()
        if tid:
            stmt2 = Running.query.filter_by(theatre_id=tid).all()
        return [x.as_dict() for x in stmt2]

    @marshal_with(resource_fields)
    def post(self):
        # // add running to database
        # // return running id
        args = parser2.parse_args()
        print(args)
        running = Running(
            theatre_id=args['theatre_id'],
            show_id=args['show_id'],
            show_name=args['show_name'],
            start=args['start'],
            end=args['end'],
            language=args['language'],
            format=args['format'],
            ticket_price=args['ticket_price']
        )
        db_session.add(running)
        db_session.commit()
        return running

    def delete(self):
        # // delete running from database
        # // return running id
        rid = parser.parse_args()['id']
        abort_if_running_doesnt_exist(rid)
        stmt = Running.query.filter_by(id=rid).one()
        # stmt.delete()
        db_session.delete(stmt)
        db_session.commit()
        return "Operation Successful", 200

    @marshal_with(resource_fields)
    def patch(self):
        # // update occupied_seats running in database
        # // return running id
        rid = parser3.parse_args()['id']
        occupied_seats = parser3.parse_args()['occupied_seats']

        # abort_if_running_doesnt_exist(rid)
        running = db_session.query(Running).filter_by(id=rid)
        running.update({'occupied_seats': occupied_seats})
        db_session.commit()
        return running.one()

    @marshal_with(resource_fields)
    def put(self):
        # // update running in database
        # // return running id
        args = parser2.parse_args()
        print(args)
        abort_if_running_doesnt_exist(args['id'])
        running = db_session.query(Running).filter_by(id=args['id'])
        running.update(args)
        db_session.commit()
        return running.one()
