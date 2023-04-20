from .. import db
from dataclasses import dataclass

@dataclass
class Training(db.Model):
    """ Training Model for storing available disciplines """
    __tablename__ = "training"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return "<Training '{}'>".format(self.title)
