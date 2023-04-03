import os
import unittest
import datetime

from flask_migrate import Migrate
from flask.cli import with_appcontext

from app import blueprint
from app.main import create_app, db
from app.main.model import user
from app.main.model.user import User
from app.main.model.discipline import Discipline
app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=user, Discipline=Discipline)

@app.cli.command()
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@with_appcontext
@app.cli.command()
def seed():
    print("SEEDING DATABASE")
    U1 = User(email='nickglas@hotmail.nl')
    db.session.add(U1)
    db.session.commit()

    D1 = Discipline(title='Pistol')
    db.session.add(D1)
    db.session.commit()