import time
from datetime import timedelta, datetime

import sqlalchemy
from celery import shared_task
from flask_restful import fields, marshal
from sqlalchemy import or_

from application.database import db_session
from application.models import Show, Theatre, Booking, Running, Review


@shared_task(ignore_result=False)
def get_csv_show(*args, **kwargs):
    import io, csv
    time.sleep(10)
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    entries = db_session.query(Show).where(Show.user_id == 1).all()
    # Write the CSV header
    csv_writer.writerow(
        ['id', 'name', 'year', 'director', 'description', 'duration', 'tags', 'ticket_price', 'format', 'language'''])

    # Write the data rows
    for entry in entries:
        csv_writer.writerow(
            [entry.id, entry.name, entry.year, entry.director, entry.description, entry.duration, entry.tags,
             entry.ticket_price, entry.format, entry.language])
    return csv_data.getvalue()


@shared_task(ignore_result=False)
def get_csv_theatre(*args, **kwargs):
    import io, csv
    time.sleep(10)
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    entries = db_session.query(Theatre.id, Theatre.name, Theatre.place, Theatre.city).where(Theatre.user_id == 1).all()
    # Write the CSV header
    csv_writer.writerow(
        ['id', 'name', 'place', 'city'])

    # Write the data rows
    for entry in entries:
        csv_writer.writerow(
            [entry.id, entry.name, entry.year, entry.director, entry.description, entry.duration, entry.tags,
             entry.ticket_price, entry.format, entry.language])
    return csv_data.getvalue()


@shared_task()
def take_stats(*args):
    now = datetime.utcnow()
    prev = now - timedelta(days=1)
    nex = now + timedelta(days=1)
    data = db_session.query(Booking.total_price, Booking.show_name, Booking.th).filter(
        or_(Booking.timestamp > prev, Booking.timestamp < nex)
    )
    data = [x.as_dict() for x in data]
    print(data)
    return data


@shared_task()
# @cache.cached(timeout=60 * 60 * 24, key_prefix='top_3')
def dynamic_pricing(*args, **kwargs):
    """
    increase the price of top three shows in number of bookings by 30%, 20% and 10%
    :return: top three shows
    """
    running = db_session.query(Booking.running_id, sqlalchemy.func.sum(Booking.person).label('tickets')).group_by(
        Booking.running_id).all()
    running = sorted(running, key=lambda x: x[1], reverse=True)
    running = marshal(running, {'running_id': fields.Integer, 'tickets': fields.Integer})
    db_session.query(Running).filter(Running.id == running[0]['running_id']).update(
        {'ticket_price': Running.ticket_price * 1.3})
    db_session.query(Running).filter(Running.id == running[1]['running_id']).update(
        {'ticket_price': Running.ticket_price * 1.2})
    db_session.query(Running).filter(Running.id == running[2]['running_id']).update(
        {'ticket_price': Running.ticket_price * 1.1})
    db_session.commit()
    return running[0:4]


@shared_task
def calculate_ratings(*args, **kwargs):
    print('Ratings Updated')
    from application.stats import combine_rating
    s, t = {}, {}
    raw = [x.as_dict() for x in db_session.query(Review).all()]
    for x in raw:
        if x['show_id'] != -1:
            if x['show_id'] in s.keys():
                s[x['show_id']].append(x['rating'])
            else:
                s[x['show_id']] = [x['rating']]
        if x['theatre_id'] != -1:
            if x['theatre_id'] in t.keys():
                t[x['theatre_id']].append(x['rating'])
            else:
                t[x['theatre_id']] = [x['rating']]
    for y in s.keys():  # y is show_id
        db_session.query(Show).filter(Show.id == y).update({'rating': combine_rating(s[y])})
    for y in t.keys():  # y is theatre_id
        th = db_session.query(Theatre).filter(Theatre.id == y).update({'rating': combine_rating(t[y])})
    db_session.commit()
