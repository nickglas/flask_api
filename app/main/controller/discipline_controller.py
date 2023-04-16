from flask import request
from flask_restx import Resource

from ..dto.discipline import DisciplineDto
from ..service.discipline_service import get_all_disciplines
from typing import Dict, Tuple

api = DisciplineDto.api
_discipline = DisciplineDto.discipline

@api.route('/')
class DisciplineList(Resource):
    @api.doc('list_of_disciplines')
    @api.marshal_list_with(_discipline, envelope='data')
    def get(self):
        """List all disciplines"""
        return get_all_disciplines()
    

@api.route('/<discipline_id>')
@api.param('discipline_id', 'The discipline identifier')
@api.response(404, 'Discipline not found.')
class User(Resource):
    @api.doc('get a discipline by id')
    def get(self, public_id):
        """get a discipline given its identifier"""
        api.abort(404)
       
