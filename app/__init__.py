from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.detection_controller import api as detection_ns
from .main.controller.discipline_controller import api as discipline_ns
from .main.controller.training_controller import api as training_ns
from .main.controller.authentication_controller import api as auth_ns


blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus (restx) web service',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(user_ns, path='/user')
api.add_namespace(detection_ns, path='/detection')
api.add_namespace(discipline_ns, path='/discipline')
api.add_namespace(training_ns, path='/training')
api.add_namespace(auth_ns, path='/authentication')