from app.main import db
from app.main.model.training import Training

def create(data):
    save_changes(data)
    return data

def save_changes(data: Training) -> None:
    db.session.add(data)
    db.session.commit()