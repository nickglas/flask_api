from app.main import db
from app.main.model.discipline import Discipline
from typing import Tuple

def get_all_disciplines():

    disciplines = Discipline.query.all()

    for d in disciplines:
        print(d.title)

    return Discipline.query.all()

# def get_discipline_by_id(public_id):
#     return Discipline.query.filter_by(public_id=public_id).first()

# def save_changes(data: Discipline) -> None:
#     db.session.add(data)
#     db.session.commit()

