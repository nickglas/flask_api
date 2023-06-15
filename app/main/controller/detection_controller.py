import os
from flask import Flask, Response, make_response, request, send_file, jsonify
from flask_restx import Resource
from werkzeug.utils import secure_filename
from PIL import Image

from app.main.model.detection import shootingResult
from ..util.dto import DetectionDto
from ..service.detection_service import detect_target, detect_target_image_cropping, detect_target_boxes, detect_target_image, detect_target_single_image_cropping
import json
import jsonpickle
from io import BytesIO
import base64
from flask_cors import cross_origin
import threading
import time
import concurrent.futures
import imghdr

api = DetectionDto.api
_detection = DetectionDto.detection

@api.route('/')
@api.response(500, 'Internal server error')
class Detection(Resource):
    """This route is for development/test purposes"""
    @api.doc('detects a target. needs base64 url as input')
    @cross_origin()
    def post(self):

        
            file = request.files['file']
            img = Image.open(file.stream)
            
            result = detect_target_image(img)

            buffer = BytesIO()

            # Save the image to the byte buffer in JPEG format
            result.save(buffer, format='JPEG')

            # Create a response object from the byte buffer data
            response = make_response(buffer.getvalue())

            # Set the content type to JPEG image
            response.headers.set('Content-Type', 'image/jpeg')

            return response
    
class multiThreadingCropping:
        def __init__(self, images) -> None:
            self.threads = []
            self.images = images
            self.results = shootingResult()

        def run_threading(self):
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

            futures = [executor.submit(detect_target_single_image_cropping, my_data) for my_data in self.images]

            # iterate over all submitted tasks and get results as they are available
            for future in concurrent.futures.as_completed(futures):
                # get the result for the next completed task
                self.results.shootingCards.append(future.result()) # blocks

            executor.shutdown() # blocks  


@api.route('/detectmultiplecroppingasync')
@api.response(500, 'Internal server error')
class DetectionMultipleCroppingAsync(Resource):
    """This route is for development/test purposes"""
    @api.doc('Needs a list of files as input. Detects each image on different thread and returns as python list')
    @cross_origin()
    def post(self):
            
            print('ran')

            uploaded_files = request.files.getlist("file")
            print(uploaded_files)
            pil_images = []
            for file in uploaded_files:                
                img = Image.open(file.stream)
                filetype = img.format

                if filetype == 'PNG':
                    rgb_image = img.convert('RGB')
                    pil_images.append(rgb_image)
                    continue

                if filetype == 'JPEG' or filetype == 'JPG' or filetype == 'WEBP':
                    pil_images.append(img)

            print(pil_images)
            multi_threading = multiThreadingCropping(pil_images)
            multi_threading.run_threading()

            # Create a JSON response with the base64 encoded image data
            response = make_response(multi_threading.results.toJSON())

            # Set the content type to application/json
            response.headers.set('Content-Type', 'application/json')

            return response
    
@api.route('/detectsinglecroppingasync')
@api.response(500, 'Internal server error')
class DetectionSingleCroppingAsync(Resource):
    """This route is for development/test purposes"""
    @api.doc('Needs a single file as input. Detects a single image')
    @cross_origin()
    def post(self):
            
            file = request.files['file']
            img = Image.open(file.stream)
            filetype = img.format

            if filetype == 'PNG':
                rgb_image = img.convert('RGB')
                result = detect_target_single_image_cropping(rgb_image)
            elif filetype == 'JPEG' or filetype == 'JPG' or filetype == 'WEBP':
                result = detect_target_single_image_cropping(img)
            else:
                return Response("{\"message\":\"Incorrect filetype\"}", status=400, mimetype='application/json')

            # Create a JSON response with the base64 encoded image data
            response = make_response(result.toJSON())

            # Set the content type to application/json
            response.headers.set('Content-Type', 'application/json')

            return response

