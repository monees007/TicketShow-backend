from flask_restful import Resource, reqparse, abort, marshal_with, fields

from application.database import db_session
from application.models import Show


def abort_if_show_doesnt_exist(sid):
    try:
        if sid != Show.query.filter_by(id=sid).one().id:
            abort(404, message="Show with ID: {} doesn't exist".format(sid))
    except Exception as e:
        abort(404, message=str(e))


parser = reqparse.RequestParser()  # for GET, DELETE requests
parser.add_argument('id', required=True, type=int, location='args')

parser2 = reqparse.RequestParser()  # for POST, PUT  requests
parser2.add_argument('id', required=False, type=int)
parser2.add_argument('name', required=True, type=str)
parser2.add_argument('rating', required=False, type=int)
parser2.add_argument('tags', required=False, type=str)
parser2.add_argument('ticket_price', required=True, type=float)
parser2.add_argument('format', required=False, type=str)
parser2.add_argument('language', required=True, type=str)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'rating': fields.Integer,
    'image_url': fields.String,
    'image_sqr': fields.String,
    'tags': fields.String,
    'ticket_price': fields.Float,
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
        show = Show(
            name=args['name'],
            rating=args['rating'],
            tags=args['tags'],
            ticket_price=args['ticket_price'],
            format=args['format'],
            language=args['language'])
        db_session.add(show)
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
        args = parser2.parse_args()
        abort_if_show_doesnt_exist(args['id'])
        show = db_session.query(Show).filter_by(id=args['id'])
        show.update(args)
        # print(show,'\n',args)
        # for x in args:
        #     print(x)
        #     show.x = args[x]
        db_session.commit()
        return show.one()
