from flask import request
from flask_restful import Resource, reqparse
from flask_security import current_user, auth_required

from application.database import db_session, get_or_create
from application.models import Show, Theatre, Running

parser = reqparse.RequestParser().add_argument('api', type=str)


class BulkShowsApi(Resource):
    @auth_required('token')
    def get(self):
        stmt = db_session.query(Show).where(Show.user_id == current_user.id).all()
        return [x.as_dict() for x in stmt]

    @staticmethod
    def post():
        try:
            json = request.get_json(force=True)
            for args in json:
                get_or_create(model=Show, name=args['name'],
                              rating=args['rating'],
                              image_url=args['image_url'],
                              image_sqr=args['image_sqr'],
                              tags=args['tags'],
                              ticket_price=args['ticket_price'],
                              format=args['format'],
                              language=args['language'],
                              user_id=current_user.id
                              )
            db_session.commit()
            return {'success': True}, 200
        except Exception as e:
            db_session.rollback()
            return {'error': str(e)}, 400


class BulkTheatreApi(Resource):
    @auth_required('token')
    def get(self):
        stmt = db_session.query(Theatre).where(Theatre.user_id == current_user.id).all()
        return [x.as_dict() for x in stmt]

    @staticmethod
    def post():
        try:
            json = request.get_json(force=True)
            for args in json:
                get_or_create(Theatre,
                              name=args['name'],
                              place=args['place'],
                              capacity=args['capacity'],
                              user_id=current_user.id)
            db_session.commit()
            return {'success': True}, 200
        except Exception as e:
            db_session.rollback()
            return {'error': str(e)}, 400


class BulkRunningApi(Resource):
    @auth_required('token')
    def get(self):
        stmt = db_session.query(Running).join(Theatre, Running.theatre_id == Theatre.theatre_id).where(
            Theatre.user_id == current_user.id).all()
        return [x.as_dict() for x in stmt]

    @staticmethod
    def post():
        try:
            json = request.get_json(force=True)
            for args in json:
                running = get_or_create(Running,
                                        theatre_id=args['theatre_id'],
                                        show_id=args['show_id'],
                                        date=args['date'])
                Running.ge(running)
                get_or_create(running)
            db_session.commit()
            return {'success': True}, 200
        except Exception as e:
            db_session.rollback()
            return {'error': str(e)}, 400
