import unittest
from run import app
from extensions import db

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        # Push application context
        self.app_context = app.app_context()
        self.app_context.push()

        self.app = app
        self.client = app.test_client()

        # Create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Remove session and pop context
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

        self.app_context.pop()