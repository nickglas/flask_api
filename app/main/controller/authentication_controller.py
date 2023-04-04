from flask import request
from flask_restx import Resource

from ..util.dto import AuthDto
from typing import Dict, Tuple

api = AuthDto.api
user_auth = AuthDto.user_auth

@api.route('/')
class GetLoggedInUser(Resource):
    """Logged in user Resource"""
    @api.doc('user login')
    def get():
        return None

@api.route('/refresh')
class UserLogin(Resource):
    """Refresh Token Resource"""
    @api.doc('Refresh token')
    def post():
        return None  

@api.route('/login')
class UserLogin(Resource):
    """User Login Resource"""
    @api.doc('user login')
    def post():
        return None   

@api.route('/logout')
class LogoutAPI(Resource):
    """Logout Resource"""
    @api.doc('user logout')
    def post():
        return None