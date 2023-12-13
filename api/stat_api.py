from flask import request, jsonify
from flask_restful import Resource

from api.booking_api import parser
from application.stats import t_ticket_sold, show_stat


class TheatreStatAPI(Resource):

    def get(self):
        tid = request.args.get('id')
        days = int(request.args.get('days'))
        """
        ## theatre
          -  no of bookings per show
          -  total tickets per day 
          -  floating average rating
          -  revenue collected
      """
        ticket_sold_per_day, revenue_per_day, label, shows = t_ticket_sold(tid, days)
        total_revenue = sum(revenue_per_day)
        ticket_sold = sum(ticket_sold_per_day)
        no_of_shows = len(shows)
        shows_names = [x for x in shows.keys()]

        bar_series = [
            {'name': "Ticket Sold", 'data': [shows[x]['seats'] for x in shows]},
            {'name': 'Revenue', 'data': [shows[x]['revenue'] for x in shows]}
        ]
        # average_rating_per_day = t_rating(tid)
        return jsonify({'ticket_sold_per_day': ticket_sold_per_day,
                        'label': label,
                        'revenue_per_day': revenue_per_day,
                        'total_revenue': total_revenue,
                        'shows_names': shows_names,
                        'bar_series': bar_series,
                        'no_of_shows': no_of_shows,
                        'ticket_sold': ticket_sold
                        })


class ShowStatAPI(Resource):
    def get(self):
        sid = parser.parse_args()['id']
        """

            :param id:
            :return: last fifteen days rating and seats
            """
        return show_stat(sid)
