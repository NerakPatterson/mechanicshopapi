import unittest
from run import create_app
from extensions import db
from flask_jwt_extended import create_access_token
from models import User


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "test-secret-key"

    # Disable caching + rate limiting in tests
    CACHE_TYPE = "null"
    CACHE_NO_NULL_WARNING = True
    RATELIMIT_ENABLED = False


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        # Create app using test config BEFORE extensions initialize
        self.app = create_app(TestConfig)

        # Push context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create fresh tables
        db.create_all()

        # Test client
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Helper: create a test user
    def create_user(self, email="test@example.com",
                    password="password123", role="admin"):
        user = User(email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    # Helper: generate JWT token
    def get_token(self, user_id=1, role="admin"):
        return create_access_token(
            identity=str(user_id),
            additional_claims={"role": role}
        )

    # Helper: Authorization header
    def auth_header(self, user_id=1, role="admin"):
        return {"Authorization": f"Bearer {self.get_token(user_id, role)}"}
