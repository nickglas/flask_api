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
