from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class DetectionDto:
    api = Namespace('detection', description='detection related operations(This route is for development/test purposes)')
    detection = api.model('detection', {
        'image': fields.String(required=True, description='base 64 url of image'),
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class TrainingDto:
    api = Namespace('training', description='training related operations')
    training = api.model('training', {
        'title': fields.String(required=True, description='training title'),
    })

class CardDto:
    api = Namespace('card', description='card related operations')
    card = api.model('card', {
        'title': fields.String(required=True, description='card title'),
        'img' : fields.String(required=False, description='card title')
    })
