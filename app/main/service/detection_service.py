import uuid
import datetime
from flask import url_for
import numpy as np
from ultralytics import YOLO
import cv2
import base64
from ultralytics.yolo.utils.plotting import Annotator
import json
from io import BytesIO

from app.main import db
from app.main.model.detection import Detection, shootingCard, shootingScore
from typing import Dict, Tuple
from PIL import Image as im

import base64


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




#TAKES A SINGLE IMAGE
def detect_image(image):

    #MODEL IS STILL STATIC CHANGE THIS WHEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    model = YOLO('runs/detect/train/weights/best.pt')

    results = model.predict(source=[image], show=False, hide_labels=False, hide_conf=False, save_txt=False,
                            save_conf=True, line_thickness=2)

    return results, model

#TAKES AN ARRAY OF IMAGES
def detect_images(images):

    #MODEL IS STILL STATIC CHANGE THIS WHEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    model = YOLO('runs/detect/train/weights/best.pt')

    results = model.predict(source=images, show=False, hide_labels=False, hide_conf=False, save_txt=False,
                            save_conf=True, line_thickness=2)

    return results, model


def convert_results_to_coordinates(results, model):
    
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

def detect_target_boxes(image):

    results, model = detect_image(image)

    return convert_results_to_coordinates(results, model)

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



def detect_target_boxes_array(images):

    results, model = detect_images(images)
    
    coordinate_results = []

    for r in results:
        coordinates = []

        boxes = r.boxes
        for box in boxes:
            conf = box.conf.numpy()[0]
            
            if box.conf.numpy()[0] < 0.4:
                continue

            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            coordinates.append((model.names[int(c)], int(c), b.tolist(), str(conf)))

        coordinate_results.append(coordinates)

    return coordinate_results

#converts PIL image to base64
def convert_to_base64(image) -> str:
    buffer = BytesIO()

    image.save(buffer, format='JPEG')
    image_data = buffer.getvalue()
    base64_data = base64.b64encode(image_data).decode('utf-8')

    return base64_data

#takes in a list of PIL images and returns an array of results
def detect_target_image_cropping(pil_images) -> Tuple[Dict[str, str], int]:

    results, model = detect_images(pil_images)


    cropped_image_results = []

    for x, r in enumerate(results):

        image = pil_images[x]

        #makes sure to crop target with highest conf
        highest_target_confidence = 0
        
        annotator = Annotator(np.ascontiguousarray(image), font='Arial.ttf')
        
        boxes = r.boxes

        for box in boxes:

            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls

            if model.names[int(c)] == 'Target':

                #check to see if the confidence is higher than the previous one
                if box.conf.numpy()[0] < highest_target_confidence:
                    continue

                highest_target_confidence = box.conf.numpy()[0]

                image = annotator.result()

                original_image = im.fromarray(image)

                cropping = (int(b[0]), int(b[1]), int(b[2]), int(b[3]))
                
        image = original_image.crop(cropping)

        cropped_image_results.append((image, cropping, original_image))

    coordinate_results = detect_target_boxes_array([t[0] for t in cropped_image_results])

    definitive_results = []

    for x, coordinate_result in enumerate(coordinate_results):

        original_image = cropped_image_results[x][2]
        cropping = cropped_image_results[x][1]

        annotator = Annotator(np.ascontiguousarray(original_image), font='Arial.ttf')

        definitive_coordinates = []

        for coordinate in coordinate_result:
            coordinate[2][0] += cropping[0]
            coordinate[2][1] += cropping[1]
            coordinate[2][2] += cropping[0]
            coordinate[2][3] += cropping[1]


            name = coordinate[0]

            if float(coordinate[3]) < 0.4:
                continue

            

            definitive_coordinates.append(coordinate)

            #filters out the black contour to keep the image clean
            if name != 'black_contour' and name != 'Target':
                color_code = get_color_code(name)
                annotator.box_label(coordinate[2], name, color=color_code)

        #annotates the target from the original cropping so that it is not covered by the other annotations 
        annotator.box_label(cropping, 'Target', get_color_code('Target'))

        image = annotator.result()  
        image = im.fromarray(image)

        definitive_results.append((definitive_coordinates, convert_to_base64(image)))
    
    return definitive_results


#filters the overlapping detections
def filter_overlapping(overlap_2d_array, distinct_areas, scores):
    print(overlap_2d_array)
    #while the highest overlapping is more then 0.7 keep removing the highest overlapping
    while np.max(overlap_2d_array[:, 0]) > 0.7:
        current_removal = [0, 0, 0, 0]
        for area in distinct_areas:

            result = overlap_2d_array[overlap_2d_array[:,1] == area]
            max_index = np.argmax(result[:,0], axis=0)

            # # Use the index to extract the corresponding innermost arrays
            biggest_overlap = result[max_index]
            if biggest_overlap[0] > 0.7 and biggest_overlap[1] > current_removal[1]:
                current_removal = biggest_overlap
        print(current_removal)
        removal_item = int(current_removal[3])

        #removes all items with the index of removal item
        mask = overlap_2d_array[:, 3] != removal_item
        overlap_2d_array = overlap_2d_array[mask]

        # #removes all items with the index of removal item
        mask = overlap_2d_array[:, 4] != removal_item
        overlap_2d_array = overlap_2d_array[mask]

        #removes the area from the distinct areas
        distinct_areas.discard(current_removal[1])

        #finally pops it from the scores array
        scores = [score for score in scores if score.id != current_removal[2]]
    return scores

#needs to two tuples of coordinates and gets the overlap percentage
def check_overlap(box1, box2):
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    x_overlap = max(0, min(box1[2], box2[2]) - max(box1[0], box2[0]))
    y_overlap = max(0, min(box1[3], box2[3]) - max(box1[1], box2[1]))
    intersection = x_overlap * y_overlap
    overlap_ratio = intersection / min(area1, area2)
    return overlap_ratio, area2

def detect_target_and_null_scores(result, model, image, scores, annotator):
        #makes sure to crop target with highest conf
    highest_target_confidence = 0
        
    boxes = result.boxes

    for box in boxes:

        b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
        c = box.cls
        confidence = box.conf.numpy()[0]

        #zeros are added here since it will not be wise to detect these when target is cropped
        if model.names[int(c)] == '0':
            scores.append(shootingScore(model.names[int(c)], int(c), b.tolist(), str(confidence)))

        if model.names[int(c)] == 'Target':

            #check to see if the confidence is higher than the previous one
            if confidence < highest_target_confidence:
                continue

            highest_target_confidence = confidence

            image = annotator.result()

            original_image = im.fromarray(image)

            cropping = (int(b[0]), int(b[1]), int(b[2]), int(b[3]))
    
    return original_image, cropping, scores, highest_target_confidence, annotator


#takes a single PIL and returns shootingCard class with base64 image and scores
def detect_target_single_image_cropping(image) -> shootingCard:

    results, model = detect_image(image)

    #array of scores
    scores = []

    #defines the annotator with the orginal image
    annotator = Annotator(np.ascontiguousarray(image), font='Arial.ttf')

    #adds the 0 scores and gets the target for second detection with cropping
    original_image, cropping, scores, highest_target_confidence, annotator = detect_target_and_null_scores(results[0], model, image, scores, annotator)

    #IF NO TARGET IS FOUND RETURN THE IMAGE
    if highest_target_confidence == 0:
        return shootingCard(convert_to_base64(image), [])
    
    
    #CROP THE IMAGE FOR BETTER DETECTION
    image = original_image

    #SECOND DETECTION FOR SCORES
    print(cropping)
    print(image.size)
    cropping_width = cropping[2] - cropping[0]
    cropping_height = cropping[3] - cropping[1]

    cropping_detection = False
    if image.size[0] * 0.97 < cropping_width or image.size[1] * 0.97 < cropping_height:
        coordinates = convert_results_to_coordinates(results, model)
    else:
        image = image.crop(cropping)
        cropping_detection = True
        coordinates = detect_target_boxes(image)
    
    
    overlap_2d_array = []

    #adds all the distinct areas from the bulletholes for overlapping later
    distinct_areas = set()
    
    for x, coordinate in enumerate(coordinates):

        #this converts the detected coordinates from the cropping image to the original image
        if cropping_detection:
            coordinate[2][0] += cropping[0]
            coordinate[2][1] += cropping[1]
            coordinate[2][2] += cropping[0]
            coordinate[2][3] += cropping[1]

        coordinate[2][0] = int(coordinate[2][0])
        coordinate[2][1] = int(coordinate[2][1])
        coordinate[2][2] = int(coordinate[2][2])
        coordinate[2][3] = int(coordinate[2][3])

        name = coordinate[0]

        #checks for condfidence higher then 0.4
        if float(coordinate[3]) < 0.4:
            continue
        
        newScore = shootingScore(*coordinate)

        scores.append(newScore)



        #ignore black contour and target for comparison
        if name != 'black_contour' and name != 'Target':

            #piece of code to check for overlapping detections
            for y, compare_coordinate in enumerate(coordinates):

                compare_coordinate[2][0] = int(compare_coordinate[2][0])
                compare_coordinate[2][1] = int(compare_coordinate[2][1])
                compare_coordinate[2][2] = int(compare_coordinate[2][2])
                compare_coordinate[2][3] = int(compare_coordinate[2][3])
                        
                #does not compare against target or black contour
                if compare_coordinate[0] == 'black_contour' or  compare_coordinate[0] == 'Target':
                    continue

                #checks for condfidence higher then 0.4
                if float(compare_coordinate[3]) < 0.4:
                    continue
                
                #does not compare against itself
                if y == x:
                    continue

                overlap_percentage, detection_size = check_overlap(coordinate[2], compare_coordinate[2])
                
                #saves the overlap perecentage, the detected size and the id of the score and the compared y
                overlap_2d_array.append((overlap_percentage, detection_size, newScore.id, y, x))

                #adds the detection size to the distinct areas
                distinct_areas.add(detection_size)

    print("test")

    #converts 2d array to numpy array
    overlap_2d_array = np.array(overlap_2d_array)

    #filters out overlapping detections
    scores = filter_overlapping(overlap_2d_array, distinct_areas, scores)

    #final annotation after filtering
    for score in scores:
        name = score.score
        if name != 'black_contour' and name != 'Target':
            color_code = get_color_code(name)
            annotator.box_label(score.location, name, color=color_code)
    

    #annotates the target from the original cropping so that it is not covered by the other annotations 
    annotator.box_label(cropping, 'Target', get_color_code('Target'))

    image = annotator.result()  
    image = im.fromarray(image)

    shooting_card = shootingCard(convert_to_base64(image), scores)
    
    return shooting_card
