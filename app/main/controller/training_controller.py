from flask import request, jsonify
from flask_restx import Resource
from ..service.training_service import create

from ..dto.training import TrainingDto

api = TrainingDto.api
_training = TrainingDto.training

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
    @api.expect(_training, validate=True)
    @api.marshal_with(_training, code=201)
    def post(self):
        """Create a new training"""
        data = create(request.json)
        return jsonify(data)
    
