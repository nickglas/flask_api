from flask import make_response, request, send_file, jsonify
from flask_restx import Resource
from werkzeug.utils import secure_filename
from PIL import Image
from ..util.dto import DetectionDto
from ..service.detection_service import detect_target
import json
import jsonpickle
from io import BytesIO

api = DetectionDto.api
_detection = DetectionDto.detection

@api.route('/')
@api.response(404, 'User not found.')
class Detection(Resource):
    
    @api.doc('detects a target. needs base64 url as input')
    def post(self):

    
        file = request.files['file']
        img = Image.open(file.stream)
        
        result = detect_target(img)

        #return jsonify(jsonpickle.encode(result))
    
        # response = make_response(result.tobytes())
        # response.headers.set('Content-Type', 'image/jpeg')


        buffer = BytesIO()

        # Save the image to the byte buffer in JPEG format
        result.save(buffer, format='JPEG')

        # Create a response object from the byte buffer data
        response = make_response(buffer.getvalue())

        # Set the content type to JPEG image
        response.headers.set('Content-Type', 'image/jpeg')

        return response


        return result.path

        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()
            return json['image']

            return detect_target(json['image'])

        else:
            return 'Content-Type not supported!'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

