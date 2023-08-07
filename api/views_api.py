from flask_restful import Resource
from sqlalchemy import desc

from application.database import db_session
from application.models import Running, Theatre, Show


class HomePageAPI(Resource):

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
