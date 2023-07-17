from flask_restful import Resource, reqparse, abort, marshal_with, fields
from sqlalchemy.exc import NoResultFound

from application.database import db_session
from application.models import Review


def abort_if_review_doesnt_exist(rid):
    try:
        Review.query.filter_by(id=rid).one()
    except NoResultFound as e:
        abort(404, message="Review with ID: {} doesn't exist".format(rid))


parser = reqparse.RequestParser()  # for GET, DELETE requests
parser.add_argument('id', required=True, type=int, location='args')

parser2 = reqparse.RequestParser()  # for POST requests
parser2.add_argument('user_id', required=True, type=int)
parser2.add_argument('show_id', required=True, type=int)
parser2.add_argument('rating', required=True, type=int)
parser2.add_argument('review', required=True, type=str)

parser3 = parser2.copy()  # for PUT requests
parser3.add_argument('id', required=True, type=int)

resource_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'show_id': fields.Integer,
    'rating': fields.Integer,
    'review': fields.String
}


class ReviewsAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # // get all reviews
        # // return all reviews
        rid = parser.parse_args()['id']
        abort_if_review_doesnt_exist(rid)
        if rid:
            stmt = Review.query.filter_by(id=rid)
            return stmt.one()

    @marshal_with(resource_fields)
    def post(self):
        # // add review to database
        # // return review id
        args = parser2.parse_args()
        review = Review(
            user_id=args['user_id'],
            show_id=args['show_id'],
            rating=args['rating'],
            review=args['review'])
        db_session.add(review)
        db_session.commit()
        return review

    def delete(self):
        # // delete review from database
        # // return review id
        rid = parser.parse_args()['id']
        abort_if_review_doesnt_exist(rid)
        stmt = Review.query.filter_by(id=rid).one()
        # stmt.delete()
        db_session.delete(stmt)
        db_session.commit()
        return "Operation Successful", 200

    @marshal_with(resource_fields)
    def put(self):
        # // update review in database
        # // return review id
        args = parser3.parse_args()
        abort_if_review_doesnt_exist(args['id'])
        review = db_session.query(Review).filter_by(id=args['id'])
        review.update(args)
        db_session.commit()
        return review.one()
