import uuid
import datetime

from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple

def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()

def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()

