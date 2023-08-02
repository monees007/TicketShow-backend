from flask_restful import Resource, reqparse, abort, marshal_with, fields
from sqlalchemy.exc import NoResultFound

from application.database import db_session, get_or_create
from application.models import Show


def abort_if_show_doesnt_exist(sid):
    try:
        Show.query.filter_by(id=sid).one()
    except NoResultFound as e:
        abort(404, message="Show with ID: {} doesn't exist".format(sid))


parser = reqparse.RequestParser()  # for GET, DELETE requests
parser.add_argument('id', required=True, type=int, location='args')

parser2 = reqparse.RequestParser()  # for POST, PUT  requests
parser2.add_argument('name', required=False, type=str)
parser2.add_argument('image_url', required=False, type=str)
parser2.add_argument('image_sqr', required=False, type=str)
parser2.add_argument('year', required=False, type=str)
parser2.add_argument('director', required=False, type=str)
parser2.add_argument('description', required=False, type=str)
parser2.add_argument('duration', required=False, type=str)
parser2.add_argument('tags', required=False, type=str)
parser2.add_argument('ticket_price', required=False, type=str)
parser2.add_argument('format', required=False, type=str)
parser2.add_argument('language', required=False, type=str)

parser3 = parser2.copy()
parser3.add_argument('id', required=True, type=int)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'rating': fields.Integer,
    'image_url': fields.String,
    'image_sqr': fields.String,
    'year': fields.String,
    'director': fields.String,
    'description': fields.String,
    'duration': fields.String,
    'tags': fields.String,
    'ticket_price': fields.String,
    'format': fields.String,
    'language': fields.String,
    # 'address': fields.String,
    # 'date_updated': fields.DateTime(dt_format='rfc822'),
}


class ShowsAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # // get all shows
        # // return all shows
        sid = parser.parse_args()['id']
        abort_if_show_doesnt_exist(sid)
        if sid:
            stmt = Show.query.filter_by(id=sid)
            return stmt.one()

    @marshal_with(resource_fields)
    def post(self):
        # // add show to database
        # // return show id
        args = parser2.parse_args()
        show = get_or_create(Show,
                             name=args['name'],
                             image_url=args['image_url'],
                             image_sqr=args['image_sqr'],
                             year=args['year'],
                             director=args['director'],
                             description=args['description'],
                             duration=args['duration'],
                             tags=args['tags'],
                             ticket_price=args['ticket_price'],
                             format=args['format'],
                             language=args['language'])
        db_session.commit()
        return show

    def delete(self):
        # // delete show from database
        # // return show id
        sid = parser.parse_args()['id']
        abort_if_show_doesnt_exist(sid)
        stmt = Show.query.filter_by(id=sid).one()
        # stmt.delete()
        db_session.delete(stmt)
        db_session.commit()
        return "Operation Successful", 200

    @marshal_with(resource_fields)
    def put(self):
        # // update show in database
        # // return show id
        args = parser3.parse_args()
        # for x in args:
        #     print(x,args[x])
        abort_if_show_doesnt_exist(args['id'])
        show = db_session.query(Show).filter_by(id=args['id'])
        print(show, '\n', args)
        show.update(args)
        print(show)
        db_session.commit()
        return show.one()
