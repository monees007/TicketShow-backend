import json
from io import BytesIO

from flask import request, Response
from flask_restful import Resource, reqparse
from flask_security import current_user, auth_required
from werkzeug.wsgi import FileWrapper

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
                get_or_create(model=Show, name=args['name'], image_url=args['image_url'], image_sqr=args['image_sqr'],
                              tags=args['tags'], ticket_price=args['ticket_price'], format=args['format'],
                              language=args['language'], user_id=current_user.id)
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
                get_or_create(Theatre, name=args['name'], place=args['place'], capacity=args['capacity'],
                              user_id=current_user.id)
            db_session.commit()
            return {'success': True}, 200
        except Exception as e:
            db_session.rollback()
            return {'error': str(e)}, 400


class BulkRunningApi(Resource):
    @auth_required('token')
    def get(self):
        stmt = (db_session.query(Running)
                .join(Theatre, Running.theatre_id == Theatre.id)
                .where(Theatre.user_id == current_user.id).all())
        return [x.as_dict() for x in stmt]

    def post(self):
        try:
            json = request.get_json(force=True)
            for args in json:
                get_or_create(Running, theatre_id=args['theatre_id'], show_id=args['show_id'], date=args['date'])
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
        # print(data)

        # def generate():
        #     data = StringIO()
        #     w = csv.writer(data)
        #
        #     # write header
        #     w.writerow((
        #         'id',
        #         'name',
        #         'image_url',
        #         'image_sqr',
        #         'tags',
        #         'ticket_price',
        #         'format',
        #         'language',
        #         'director',
        #         'description',
        #         'rating',
        #         'year',
        #         'duration',
        #         'user_id',
        #         'timestamp'
        #     ))
        #     yield data.getvalue()
        #     data.seek(0)
        #     data.truncate(0)
        #
        #     # write each log item
        #     for item in log:
        #         w.writerow((
        #             item['id'],
        #                 item['name'],
        #                 item['image_url'],
        #                 item['image_sqr'],
        #                 item['tags'],
        #                 item['ticket_price'],
        #                 item['format'],
        #                 item['language'],
        #                 item['director'],
        #                 item['description'],
        #                 item['rating'],
        #                 item['year'],
        #                 item['duration'],
        #                 item['user_id'],
        #                 item['timestamp']
        #                 # format datetime as string
        #             ))
        #             yield data.getvalue()
        #             data.seek(0)
        #             data.truncate(0)
        #
        #     response = Response(generate(), mimetype='text/csv')
        #     # add a filename
        #     response.headers.set("Content-Disposition", "attachment", filename="export.csv")
        #     return response
        #
        # def get2(self):
        b = FileWrapper(BytesIO(json.dumps(log, indent=4).encode('utf-8')))
        header = {'Content-Disposition': 'attachment; filename="credentials.json"'}
        return Response(b, mimetype="text/plain", direct_passthrough=True, headers=header)
