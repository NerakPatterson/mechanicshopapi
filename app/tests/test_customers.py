import unittest
from run import app

class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # GET PAGINATED CUSTOMERS
    def test_get_customers(self):
        response = self.client.get("/customers?page=1&per_page=10")
        self.assertEqual(response.status_code, 200)

    # CREATE CUSTOMER
    def test_create_customer_missing_fields(self):
        payload = {
            "email": "missingname@example.com"
        }
        response = self.client.post("/customers", json=payload)
        self.assertIn(response.status_code, [400, 409])

    # GET CUSTOMER TICKETS (AUTH REQUIRED)
    def test_get_my_tickets_unauthorized(self):
        response = self.client.get("/customers/my-tickets")
        # Without a token, this should fail
        self.assertIn(response.status_code, [401, 403])

    # GET SINGLE CUSTOMER
    def test_get_customer_not_found(self):
        response = self.client.get("/customers/999999")
        self.assertEqual(response.status_code, 404)

    # UPDATE CUSTOMER
    def test_update_customer_not_found(self):
        payload = {
            "name": "Updated Customer"
        }
        response = self.client.put("/customers/999999", json=payload)
        self.assertEqual(response.status_code, 404)

    # DELETE CUSTOMER
    def test_delete_customer_not_found(self):
        response = self.client.delete("/customers/999999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()