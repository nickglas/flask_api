from flask_restx import Namespace, fields

class CardDto:
    api = Namespace('card', description='card related operations')
    training = api.model('card', {
        'title': fields.String(required=True, description='title'),
        'img' : fields.String(required=False, description='card title')
    })