from datetime import datetime

from flask_restful import Resource, reqparse, abort, marshal_with, fields

from application.database import db_session
from application.models import Running


def abort_if_running_doesnt_exist(rid):
    try:
        if rid != Running.query.filter_by(id=rid).one().id:
            abort(404, message="Running with ID: {} doesn't exist".format(rid))
    except Exception as e:
        abort(404, message=str(e))


parser = reqparse.RequestParser()  # for GET, DELETE requests
parser.add_argument('id', required=True, type=int, location='args')

parser2 = reqparse.RequestParser()  # for POST, PUT  requests
parser2.add_argument('id', required=False, type=int)
parser2.add_argument('theatre_id', required=True, type=int)
parser2.add_argument('show_id', required=True, type=int)
parser2.add_argument('date', required=True, type=datetime)

resource_fields = {
    'id': fields.Integer,
    'theatre_id': fields.Integer,
    'show_id': fields.Integer,
    'date': fields.DateTime
}


class RunningAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # // get all runnings
        # // return all runnings
        rid = parser.parse_args()['id']
        abort_if_running_doesnt_exist(rid)
        if rid:
            stmt = Running.query.filter_by(id=rid)
            return stmt.one()

    @marshal_with(resource_fields)
    def post(self):
        # // add running to database
        # // return running id
        args = parser2.parse_args()
        running = Running(
            theatre_id=args['theatre_id'],
            show_id=args['show_id'],
            date=args['date'])
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
