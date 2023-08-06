from flask_restful import Resource, reqparse, abort, marshal_with, fields
from sqlalchemy.exc import NoResultFound

from api.theater_api import abort_if_theatre_doesnt_exist
from application.database import db_session
from application.models import Running


def abort_if_running_doesnt_exist(rid):
    try:
        Running.query.filter_by(id=rid).one()
    except NoResultFound as e:
        abort(404, "Running with ID: {} doesn't exist")


parser = reqparse.RequestParser()  # for GET, DELETE requests
parser.add_argument('id', required=True, type=int, location='args')

parser2 = reqparse.RequestParser()  # for POST, PUT  requests
parser2.add_argument('id', required=False, type=int)
parser2.add_argument('theatre_id', required=True, type=int)
parser2.add_argument('show_id', required=True, type=int)
parser2.add_argument('show_name', required=False, type=str)
parser2.add_argument('start', required=False, type=str)
parser2.add_argument('end', required=False, type=str)
parser2.add_argument('language', required=False, type=str)
parser2.add_argument('format', required=False, type=str)
parser2.add_argument('ticket_price', required=False, type=str)

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

}


class RunningAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # // get all runnings
        # // return all runnings
        tid = parser.parse_args()['id']
        abort_if_theatre_doesnt_exist(tid)
        if tid:
            stmt = Running.query.filter_by(theatre_id=tid).all()
        return [x.as_dict() for x in stmt]

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
    def put(self):
        # // update running in database
        # // return running id
        args = parser2.parse_args()
        abort_if_running_doesnt_exist(args['id'])
        running = db_session.query(Running).filter_by(id=args['id'])
        running.update(args)
        db_session.commit()
        return running.one()
