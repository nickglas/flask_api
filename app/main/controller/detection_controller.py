import os
from flask import Flask, make_response, request, send_file, jsonify
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

# Test classes niet janken
class testCard:
    def __init__(self, url, scores) -> None:
        self.base64Url = url
        self.scores = scores


class testTraining:

    def __init__(self, title) -> None:
        self.title = title
        self.cards = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

     

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
        
@api.route('/detect')
@api.response(500, 'Internal server error')
class Detection(Resource):
    """This route is for development/test purposes"""
    @api.doc('detects a target. needs base64 url as input')
    def post(self):
            file = request.files['file']
            img = Image.open(file.stream)

            result = detect_target(img)

            buffer = BytesIO()
            result.save(buffer, format='JPEG')
            image_data = buffer.getvalue()

            # Encode the image data as a base64 string
            base64_data = base64.b64encode(image_data).decode('utf-8')

            # Create a JSON response with the base64 encoded image data
            response_data = {'image': base64_data}
            response = make_response(jsonify(response_data))

            # Set the content type to application/json
            response.headers.set('Content-Type', 'application/json')

            return response
    
@api.route('/detectMultiple')
@api.response(500, 'Internal server error')
class Detection(Resource):
    """This route is for development/test purposes"""
    @api.doc('detects a target. needs base64 url as input')
    def post(self):
            
            print('ran')
            training = testTraining('Some title') 

            uploaded_files = request.files.getlist("file")

            for file in uploaded_files:
                print(file)
                buffer = BytesIO()
                img = Image.open(file.stream)
                cardScore, result = detect_target(img)
                result.save(buffer, format='JPEG')
                image_data = buffer.getvalue()
                base64_data = base64.b64encode(image_data).decode('utf-8')
                card = testCard(base64_data, cardScore)
                training.cards.append(card)


            # write to file for debug
            f = open("debug.txt", "a")
            f.write(training.toJSON())
            f.close()

            # Create a JSON response with the base64 encoded image data
            response = make_response(training.toJSON())

            # Set the content type to application/json
            response.headers.set('Content-Type', 'application/json')

            return response
        

@api.route('/hits')
class DetectionCoordinates(Resource):
    @api.doc('detects a target. return coordinates of the target and shots')
    @cross_origin()
    def post(self):

        try:
            
            print(request.files.getlist('file'))

            file = request.files['file']


            img = Image.open(file.stream)
            
            result = detect_target_boxes(img)

            return result
        except Exception as e:
            

            return e
            pass


@api.route('/detectmultiplecropping')
@api.response(500, 'Internal server error')
class DetectionMultipleCropping(Resource):
    """This route is for development/test purposes"""
    @api.doc('Detects multiple images needs formdata files as input')
    def post(self):
            
            print('ran')
            result = shootingResult() 

            uploaded_files = request.files.getlist("file")
            pil_images = []
            for file in uploaded_files:
                print(file)
                buffer = BytesIO()
                img = Image.open(file.stream)
                pil_images.append(img)


            results = detect_target_image_cropping(pil_images)


            return results
       
def single_thread(image):
    cardScore, result = detect_target(image)
    buffer = BytesIO()
    result.save(buffer, format='JPEG')
    image_data = buffer.getvalue()
    base64_data = base64.b64encode(image_data).decode('utf-8')
    card = testCard(base64_data, cardScore)
    return card

class multiThreading:
        def __init__(self, images) -> None:
            self.threads = []
            self.images = images
            self.results = testTraining('Resultaten')

        def run_threading(self):
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

            futures = [executor.submit(single_thread, my_data) for my_data in self.images]

            # iterate over all submitted tasks and get results as they are available
            for future in concurrent.futures.as_completed(futures):
                # get the result for the next completed task
                self.results.cards.append(future.result()) # blocks

            executor.shutdown() # blocks  


@api.route('/detectmultipleasync')
@api.response(500, 'Internal server error')
class DetectionMultipleAsync(Resource):
    """This route is for development/test purposes"""
    @api.doc('Needs a list of files as input. Detects each image on different thread and returns as proper json')
    def post(self):
            
            print('ran')

            uploaded_files = request.files.getlist("file")
            pil_images = []
            for file in uploaded_files:
                print(file)
                img = Image.open(file.stream)
                pil_images.append(img)

            multi_threading = multiThreading(pil_images)
            multi_threading.run_threading()

            # Create a JSON response with the base64 encoded image data
            response = make_response(multi_threading.results.toJSON())

            # Set the content type to application/json
            response.headers.set('Content-Type', 'application/json')

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
    def post(self):
            
            print('ran')

            uploaded_files = request.files.getlist("file")
            print(uploaded_files)
            pil_images = []
            for file in uploaded_files:                
                img = Image.open(file.stream)
                filetype = img.format

                if filetype == 'PNG':
                    # Create a new filename for the JPEG image
                    rgb_image = img.convert('RGB')

                    new_filename = os.path.splitext('myimage.png')[0] + '.jpg'

                    # Save the image in JPEG format
                    rgb_image.save(new_filename, 'JPEG')
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
