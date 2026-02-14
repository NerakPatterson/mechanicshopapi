from app.tests.base import BaseTestCase
from extensions import db
from models import User


class TestUsers(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Create a user for login + GET/PUT/DELETE tests
        self.user = User(
            email="john@example.com",
            role="admin"
        )
        self.user.set_password("password123")
        db.session.add(self.user)
        db.session.commit()

        self.headers = self.auth_header()  # admin token

    # REGISTER
    def test_register_user_success(self):
        payload = {
            "email": "new@example.com",
            "password": "password123",
            "role": "customer"
        }
        response = self.client.post("/users/register", json=payload)
        self.assertIn(response.status_code, [200, 201])

    def test_register_user_missing_fields(self):
        payload = {"email": "missingname@example.com"}  
        response = self.client.post("/users/register", json=payload)
        self.assertEqual(response.status_code, 400)

    # LOGIN
    def test_login_success(self):
        payload = {
            "email": "john@example.com",
            "password": "password123"
        }
        response = self.client.post("/users/login", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_login_invalid_credentials(self):
        payload = {
            "email": "wrong@example.com",
            "password": "badpass"
        }
        response = self.client.post("/users/login", json=payload)
        self.assertIn(response.status_code, [400, 401])

    # GET ALL USERS
    def test_get_all_users(self):
        response = self.client.get("/users", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # GET SINGLE USER
    def test_get_single_user_not_found(self):
        response = self.client.get("/users/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # UPDATE USER
    def test_update_user_not_found(self):
        payload = {"role": "customer"}  # valid field
        response = self.client.put("/users/999999", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # DELETE USER
    def test_delete_user_not_found(self):
        response = self.client.delete("/users/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)
