import uuid
import datetime
import numpy as np
from ultralytics import YOLO
import cv2
import base64
from ultralytics.yolo.utils.plotting import Annotator

from app.main import db
from app.main.model.detection import Detection
from typing import Dict, Tuple
from PIL import Image as im

def detect_target(image) -> Tuple[Dict[str, str], int]:

    model = YOLO('C:\\projects\\flask_api\\runs\\detect\\train\\weights\\best.pt')

    results = model.predict(source=[image], show=False, hide_labels=False, hide_conf=False, save_txt=False,
                            save_conf=True, line_thickness=2)


    # response_object = {
    #     'status': 'success',
    #     'message': 'Successfully detected target.',
    # }

    res = getScoreConfidence(results[0])

    for r in results:
        
        annotator = Annotator(np.ascontiguousarray(image))
        
        boxes = r.boxes
        for box in boxes:
            
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            annotator.box_label(b, model.names[int(c)])
 
    image = annotator.result()  

    return im.fromarray(image)


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
        self.confidence = confidence

        for x in range(11):

            if label == 'Bullet_'+str(x):
                self.score = x


def save_changes(data: Detection) -> None:
    db.session.add(data)
    db.session.commit()

