import json
from io import BytesIO

from flask import request, Response
from flask_restful import Resource, reqparse
from flask_security import current_user, auth_required, auth_token_required
from werkzeug.wsgi import FileWrapper

from application.database import db_session
from application.models import Show, Theatre, Running

parser = reqparse.RequestParser().add_argument('api', type=str)


class BulkShowsApi(Resource):
    @auth_token_required
    def get(self):
        stmt = db_session.query(Show).where(Show.user_id == current_user.id).all()
        return [x.as_dict() for x in stmt]

    @staticmethod
    @auth_token_required
    def post():
        try:
            for args in request.get_json(force=True):
                if 'abc' not in str(args['id']):
                    del args['timestamp']
                    show = Show.query.filter_by(id=args['id'])
                    show.update(args)
                else:
                    del args['id']
                    try:
                        db_session.add(Show(name=args['name'],
                                            image_url=args['image_url'],
                                            image_sqr=args['image_sqr'],
                                            year=args['year'],
                                            director=args['director'],
                                            description=args['description'],
                                            duration=args['duration'],
                                            tags=args['tags'],
                                            ticket_price=args['ticket_price'],
                                            format=args['format'],
                                            language=args['language'],
                                            user_id=current_user.id))
                    except Exception as e:
                        print(e)
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

    @auth_required('token')
    def post(self):
        try:
            for args in request.get_json(force=True):
                if 'abc' not in str(args['id']):
                    del args['timestamp']
                    show = Theatre.query.filter_by(id=args['id'])
                    show.update(args)
                else:
                    del args['id']
                    try:
                        db_session.add(Theatre(name=args['name'],
                                               place=args['place'],
                                               city=args['city'],
                                               user_id=current_user.id))
                    except Exception as e:
                        print(e)
            db_session.commit()
            return {'success': True}, 200
        except Exception as e:
            db_session.rollback()
            return {'error': str(e)}, 400


class BulkRunningApi(Resource):
    @auth_required('token')
    def get(self):
        pack = {}
        # //get theatre id of current_user
        theatre_ids = db_session.query(Theatre).where(Theatre.user_id == current_user.id).all()
        theatre_ids = [x.id for x in theatre_ids]
        for x in theatre_ids:
            pack[x] = [x.as_dict() for x in (db_session.query(Running).join(Theatre, Running.theatre_id == x).all())]
        return pack

    @auth_required('token')
    def post(self):
        try:
            theatre_ids = request.get_json(force=True)
            for ids in theatre_ids:
                for args in theatre_ids[ids]:
                    if 'abc' not in str(args['id']):
                        if 'timestamp' in args.keys():
                            del args['timestamp']
                        show = Running.query.filter_by(id=args['id'])
                        show.update(args)
                        db_session.commit()
                    else:
                        del args['id']
                        try:
                            db_session.add(
                                Running(theatre_id=args['theatre_id'], show_id=args['show_id'], date=args['date']))
                        except Exception as e:
                            print(e)
            db_session.commit()
            return {'success': True}, 200
        except Exception as e:
            db_session.rollback()
            return {'error': str(e)}, 400


class ExportCSV(Resource):
    def get(self):
        # api = parser.parse_args()['api']
        print(12)
        # if api == 'shows':
        stmt = db_session.query(Show).where(Show.user_id == current_user.id).all()
        log = [x.as_dict() for x in stmt]
        b = FileWrapper(BytesIO(json.dumps(log, indent=4).encode('utf-8')))
        header = {'Content-Disposition': 'attachment; filename="credentials.json"'}
        return Response(b, mimetype="text/plain", direct_passthrough=True, headers=header)
