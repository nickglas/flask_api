from .. import db
from dataclasses import dataclass

@dataclass
class Discipline(db.Model):
    """ discipline Model for storing available disciplines """
    __tablename__ = "discipline"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return "<Discipline '{}'>".format(self.title)
