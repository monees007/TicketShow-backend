from flask_restful import Resource, fields, marshal_with
from flask_security import current_user, auth_token_required

from application.database import db_session
from application.models import Role, RolesUsers

resource_fields = {
    'email': fields.String,
    'username': fields.String,
    'role': fields.String,
}


class UserAPI(Resource):
    @marshal_with(resource_fields)
    @auth_token_required
    def get(self):
        res = (db_session.query(Role.name).join(RolesUsers, RolesUsers.role_id == Role.id).filter(
            RolesUsers.user_id == current_user.id).first())
        role = res[0] if res else 'user'
        return {'email': current_user.email, 'username': current_user.username, 'role': role}
