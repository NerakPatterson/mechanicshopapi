from app.tests.base import BaseTestCase
from extensions import db
from models import Customer


class TestCustomers(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Create a sample customer for GET/PUT/DELETE tests
        self.customer = Customer(
            name="Jane Customer",
            email="jane@customer.com",
            phone="555-1234",
            address=None
        )
        db.session.add(self.customer)
        db.session.commit()

        self.headers = self.auth_header()  # admin token

    # GET PAGINATED CUSTOMERS
    def test_get_customers(self):
        response = self.client.get("/customers?page=1&per_page=10", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # CREATE CUSTOMER 
    def test_create_customer_missing_fields(self):
        payload = {"email": "missingname@example.com"} 
        response = self.client.post("/customers", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    # GET CUSTOMER TICKETS (AUTH REQUIRED)
    def test_get_my_tickets_unauthorized(self):
        # No token
        response = self.client.get("/customers/my-tickets")
        self.assertIn(response.status_code, [401, 403])

    # GET SINGLE CUSTOMER
    def test_get_customer_not_found(self):
        response = self.client.get("/customers/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # UPDATE CUSTOMER 
    def test_update_customer_not_found(self):
        payload = {"name": "Updated Customer"}
        response = self.client.put("/customers/999999", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # DELETE CUSTOMER 
    def test_delete_customer_not_found(self):
        response = self.client.delete("/customers/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)
