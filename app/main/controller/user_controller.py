from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
from ..service.user_service import get_a_user

api = UserDto.api
_user = UserDto.user

@api.route('/')
@api.response(200, 'Ok')
@api.response(401, 'Forbidden')
@api.response(403, 'Unauthorized')
@api.response(500, 'Internal server error.')
class User(Resource):
    @api.doc('get logged in user info')
    def get(self, public_id):
        """get the logged in user info"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user



