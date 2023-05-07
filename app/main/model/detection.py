from .. import db
import json

class Detection(db.Model):
    """ Detection Model for storing detection related details """
    __tablename__ = "detection"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(9999), unique=True, nullable=False)

    def __repr__(self):
        return "<Detection '{}'>".format(self.detection)
    



# Nieuwe test classes voor de nieuwe detectie
class shootingResult:
    def __init__(self) -> None:
        self.shootingCards = []
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

class shootingCard:

    def __init__(self, url, scores) -> None:
        self.url = url
        self.scores = scores
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)



class shootingScore:
         
        def __init__(self, score, classification, location, confidence) -> None:
            self.score = score
            self.classification = classification
            self.location = location
            self.confidence = confidence

