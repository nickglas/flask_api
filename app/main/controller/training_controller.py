from flask import request
from flask_restx import Resource

from ..dto.training import TrainingDto

api = TrainingDto.api

@api.route('/')
class Training(Resource):

    @api.doc('list of all training')
    def get(self):
        """List all training"""
        return None

    @api.doc('Post new training')
    def post(self):
        return None