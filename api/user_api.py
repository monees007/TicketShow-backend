from flask_restful import Resource, fields, marshal_with
from flask_security import current_user

from application.database import db_session
from application.models import User, Role, RolesUsers

resource_fields = {
    'email': fields.String,
    'username': fields.String,
    'name': fields.String,
}


class UserAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return (db_session.query(User.email, User.username, Role.name)
                .join(RolesUsers, RolesUsers.user_id == User.id).join(Role, Role.id == RolesUsers.role_id)
                .where(User.id == current_user.id).first())
