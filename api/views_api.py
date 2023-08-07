from flask import request
from flask_restful import Resource, marshal
from sqlalchemy import desc, or_

from api import show_api, theater_api
from application import cache
from application.database import db_session
from application.models import Running, Theatre, Show


class HomePageAPI(Resource):
    @cache.cached(timeout=50)
    def get(self):
        """
        datastructure of return:
        [
          {  theatre_id : [ theatre , show , show...]},
          t_order // order of theatres in dec order of rating
        ]
        """
        appendage = [{}]
        t_order = []
        theater_ids = (
            db_session.query(Running.theatre_id).join(Theatre, Running.theatre_id == Theatre.id).order_by(
                desc(Theatre.rating)).all())
        for x in theater_ids:
            tid = x[0]
            if tid not in t_order:
                t_order.append(tid)

            theatre_o = db_session.query(Theatre).where(Theatre.id == tid).one().as_dict()
            shows = db_session.query(Show).join(Running, Running.show_id == Show.id).where(
                Running.theatre_id == tid).all()
            shows = [x.as_dict() for x in shows]
            appendage[0][tid] = {0: theatre_o, 1: shows}
        appendage.append(t_order)
        return appendage


class SearchAPI(Resource):
    # @cache.cached(timeout=50)
    def get(self):
        """
        param{
            search_string: string to search for
            search_type: 0 for show, 1 for theatre
        }
        datastructure of return:
        [ array of dictionaries of show/theatre objects  ]
        """
        search_string = request.args.get('search_string')
        search_type = request.args.get('search_type')
        print(search_type, search_string)
        if search_type == '0':
            stmt = db_session.query(Show.name, Show.director).filter(
                or_(
                    Show.name.like('%' + search_string + '%'),
                    Show.director.like('%' + search_string + '%'),
                    # Show.description.like('%' + search_string + '%'),
                    Show.tags.like('%' + search_string + '%'),
                    Show.format.like('%' + search_string + '%')
                )).join(Running, Show.id == Running.show_id).distinct().all()
            #     return marshal(stmt, show_api.resource_fields)
            # if search_type == 1:
            stmt2 = db_session.query(Theatre).filter(
                or_(
                    Theatre.name.like('%' + search_string + '%'),
                    Theatre.place.like('%' + search_string + '%'),
                )).distinct().all()
            return marshal(stmt, show_api.resource_fields) + marshal(stmt2, theater_api.resource_fields)
