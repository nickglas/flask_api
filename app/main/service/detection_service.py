import uuid
import datetime
from flask import url_for
import numpy as np
from ultralytics import YOLO
import cv2
import base64
from ultralytics.yolo.utils.plotting import Annotator
import json

from app.main import db
from app.main.model.detection import Detection
from typing import Dict, Tuple
from PIL import Image as im

def detect_target(image) -> Tuple[Dict[str, str], int]:

    results, model = detect_image(image)

    for r in results:
        annotator = Annotator(np.ascontiguousarray(image))

        boxes = r.boxes
        for box in boxes:
            
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            annotator.box_label(b, model.names[int(c)])
 
    image = annotator.result()  

    return getShotScore(results[0]), im.fromarray(image)



def detect_target_image(image) -> Tuple[Dict[str, str], int]:

    # image = np.asarray(image)

    # image = cv2.resize(image, (640, 640), interpolation=cv2.INTER_AREA)

    # image = im.fromarray(image)

    results, model = detect_image(image)

    for r in results:
        
        annotator = Annotator(np.ascontiguousarray(image), font='Arial.ttf')
        
        boxes = r.boxes
        for box in boxes:

            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls

            if box.conf.numpy()[0] < 0.4:
                continue

            name = model.names[int(c)]

            #filters out the black contour to keep the image clean
            if name != 'black_contour':
                color_code = get_color_code(name)
                annotator.box_label(b, name, color=color_code)
            
 
    image = annotator.result()  

    return im.fromarray(image)

def get_color_code(name):
    if name == '10':
        return (0, 0, 255)
    elif name == '9':
        return (0, 255, 0)
    elif name == '8':
        return (255, 0, 0)
    elif name == '7':
        return (0, 255, 255)
    elif name == '6':
        return (255, 0, 255)
    elif name == '5':
        return (255, 255, 0)
    elif name == '4':
        return (0, 0, 128)
    elif name == '3':
        return (0, 128, 0)
    elif name == '2':
        return (128, 0, 0)
    elif name == '1':
        return (0, 128, 128)
    elif name == '0':
        return (128, 0, 128)
    elif name == 'Target':
        return (0, 200, 200)
    else:
        return (0, 0, 0)





def detect_image(image):

    #MODEL IS STILL STATIC CHANGE THIS WHEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    model = YOLO('runs/detect/train/weights/best.pt')

    results = model.predict(source=[image], show=False, hide_labels=False, hide_conf=False, save_txt=False,
                            save_conf=True, line_thickness=2)

    return results, model


def detect_target_boxes(image):

    # image = np.asarray(image)

    # image = cv2.resize(image, (640, 640), interpolation=cv2.INTER_AREA)

    # image = im.fromarray(image)

    results, model = detect_image(image)
    
    coordinates = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = box.conf.numpy()[0]
            
            if box.conf.numpy()[0] < 0.4:
                continue

            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            coordinates.append((model.names[int(c)], int(c), b.tolist(), str(conf)))

    return coordinates

def getShotScore(prediction):
    results = []
    classes = prediction.names

    for box in prediction.boxes:
        conf = box.conf.numpy()[0]
        shotClass = classes[int(box.cls.numpy()[0])]

        if shotClass == 'Target' or shotClass == 'black_contour':
            continue

        results.append(ShotResult(shotClass, conf))

    return results

def getScoreConfidence(prediction):

    results = []
    classes = prediction.names

    # utils.printMessage(prediction.names, True)

    for box in prediction.boxes:
        conf = box.conf.numpy()[0]
        shotClass = classes[int(box.cls.numpy()[0])]

        if shotClass == 'Target':
            continue

        results.append(ShotResult(shotClass, conf))

    result = Result(results)

    return result

class Result:

    def __init__(self, shotResults):
        self.shotResults = shotResults

    def getTotalScore(self):
        score = 0

        for shot in self.shotResults:
            score += shot.score

        return score


class ShotResult:

    def __init__(self, label, confidence):
        self.label = label
        # self.confidence = confidence

        for x in range(11):

            if label == str(x):
                self.score = x


def save_changes(data: Detection) -> None:
    db.session.add(data)
    db.session.commit()


def detect_target_image_cropping(image) -> Tuple[Dict[str, str], int]:

    results, model = detect_image(image)

    for r in results:
        
        annotator = Annotator(np.ascontiguousarray(image), font='Arial.ttf')
        
        boxes = r.boxes
        for box in boxes:

            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls

            if model.names[int(c)] == 'Target':

                image = annotator.result()

                original_image = im.fromarray(image)

                cropping = (int(b[0]), int(b[1]), int(b[2]), int(b[3]))
                
                image = original_image.crop(cropping)

    coordinates = detect_target_boxes(image)

    annotator = Annotator(np.ascontiguousarray(original_image), font='Arial.ttf')

    for coordinate in coordinates:
        coordinate[2][0] += cropping[0]
        coordinate[2][1] += cropping[1]
        coordinate[2][2] += cropping[0]
        coordinate[2][3] += cropping[1]


        name = coordinate[0]

        if float(coordinate[3]) < 0.4:
            continue

        #filters out the black contour to keep the image clean
        if name != 'black_contour' and name != 'Target':
            color_code = get_color_code(name)
            annotator.box_label(coordinate[2], name, color=color_code)

    annotator.box_label(cropping, 'Target', get_color_code('Target'))

      
    image = annotator.result()  

    return im.fromarray(image)