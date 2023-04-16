from flask import request
from flask_restx import Resource

from ..dto.training import TrainingDto

api = TrainingDto.api

@api.route('/')
@api.response(200, 'Ok')
@api.response(201, 'Created')
@api.response(401, 'Forbidden')
@api.response(500, 'Internal server error')
class Training(Resource):

    @api.doc('list of all training')
    def get(self):
        """List all training"""
        return None

    @api.doc('Post new training')
    def post(self):
        """Create a new training"""
        return None