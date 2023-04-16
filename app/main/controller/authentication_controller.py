from flask import request
from flask_restx import Resource

from ..util.dto import AuthDto
from typing import Dict, Tuple

api = AuthDto.api
user_auth = AuthDto.user_auth

@api.route('/')
@api.response(201, 'Ok')
@api.response(401, 'Forbidden')
@api.response(403, 'Unauthorized')
@api.response(500, 'Internal server error')
class GetLoggedInUser(Resource):
    """Logged in user Resource"""
    @api.doc('Get logged in user')
    def get():
        """Gets the logged in user info"""
        return None

@api.route('/refresh')
@api.response(201, 'Created')
@api.response(401, 'Forbidden')
@api.response(500, 'Internal server error')
class UserLogin(Resource):
    """Refresh Token Resource"""
    @api.doc('Refresh token')
    def post():
        """Refresh token"""
        return None  

@api.route('/login')
@api.response(201, 'Created')
@api.response(403, 'Unauthorized')
class UserLogin(Resource):
    """User Login Resource"""
    @api.doc('user login')
    def post():
        """Login user"""
        return None   

@api.route('/logout')
@api.response(200, 'Ok')
@api.response(401, 'Forbidden')
class LogoutAPI(Resource):
    """Logout Resource"""
    @api.doc('user logout')
    def post():
        """Logout user"""
        return None