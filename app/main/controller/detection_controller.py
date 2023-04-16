from flask import make_response, request, send_file, jsonify
from flask_restx import Resource
from werkzeug.utils import secure_filename
from PIL import Image
from ..util.dto import DetectionDto
from ..service.detection_service import detect_target, detect_target_boxes
import json
import jsonpickle
from io import BytesIO

api = DetectionDto.api
_detection = DetectionDto.detection

@api.route('/')
@api.response(500, 'Internal server error')
class Detection(Resource):
    """This route is for development/test purposes"""
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

@api.route('/hits')
class DetectionCoordinates(Resource):

    @api.doc('detects a target. return coordinates of the target and shots')
    def post(self):
        file = request.files['file']
        img = Image.open(file.stream)
        
        result = detect_target_boxes(img)

        return jsonify(result)
