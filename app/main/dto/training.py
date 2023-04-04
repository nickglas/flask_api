from flask_restx import Namespace, fields


class TrainingDto:
    api = Namespace('training', description='training related operations')
    training = api.model('training', {
        'title': fields.String(required=True, description='title')
    })