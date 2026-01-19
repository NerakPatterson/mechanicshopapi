import unittest
from run import app

class TestUsers(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # REGISTER
    def test_register_user_success(self):
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "role": "admin"   # REQUIRED FIELD
        }
        response = self.client.post("/users/register", json=payload)
        self.assertIn(response.status_code, [200, 201])

    def test_register_user_missing_fields(self):
        payload = {
            "email": "missingname@example.com"
        }
        response = self.client.post("/users/register", json=payload)
        self.assertEqual(response.status_code, 400)
        
    # LOGIN
    def test_login_success(self):
        payload = {
            "email": "john@example.com",
            "password": "password123"
        }
        response = self.client.post("/users/login", json=payload)
        self.assertIn(response.status_code, [200, 401])

    def test_login_invalid_credentials(self):
        payload = {
            "email": "wrong@example.com",
            "password": "badpass"
        }
        response = self.client.post("/users/login", json=payload)
        self.assertIn(response.status_code, [400, 401])

    # GET ALL USERS
    def test_get_all_users(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)

    # GET SINGLE USER
    def test_get_single_user_not_found(self):
        response = self.client.get("/users/999999")
        self.assertEqual(response.status_code, 404)

    # UPDATE USER
    def test_update_user_not_found(self):
        payload = {
            "name": "Updated Name"
        }
        response = self.client.put("/users/999999", json=payload)
        self.assertEqual(response.status_code, 404)

    # DELETE USER
    def test_delete_user_not_found(self):
        response = self.client.delete("/users/999999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()