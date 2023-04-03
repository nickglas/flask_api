from .. import db

class Detection(db.Model):
    """ Detection Model for storing detection related details """
    __tablename__ = "detection"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(9999), unique=True, nullable=False)

    def __repr__(self):
        return "<Detection '{}'>".format(self.detection)