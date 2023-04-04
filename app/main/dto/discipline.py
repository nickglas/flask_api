from flask_restx import Namespace, fields


class DisciplineDto:
    api = Namespace('discipline', description='discipline related operations')
    discipline = api.model('discipline', {
        'title': fields.String(required=True, description='title')
    })