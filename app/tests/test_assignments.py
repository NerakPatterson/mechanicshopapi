from app.tests.base import BaseTestCase
from extensions import db
from models import Customer, Vehicle, ServiceTicket, Mechanic


class TestAssignments(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Create customer
        self.customer = Customer(
            name="Jane Customer",
            email="jane@example.com",
            phone="555-1234"
        )
        db.session.add(self.customer)
        db.session.flush() # ensures self.customer.id is available

        # Create vehicle
        self.vehicle = Vehicle(
            vin="123456789ABCDEFG",
            make="Toyota",
            model="Camry",
            year=2020,
            customer_id=self.customer.id
        )
        db.session.add(self.vehicle)
        db.session.flush() # ensure self.vehicle.id exists

        # Create mechanic
        self.mechanic = Mechanic(
            name="John Mechanic",
            email="john@shop.com",
            salary=55000
        )
        db.session.add(self.mechanic)
        db.session.flush()

        # Create ticket
        self.ticket = ServiceTicket(
            vehicle_id=self.vehicle.id,
            description="Test ticket",
            status="open",
            cost=0
        )
        db.session.add(self.ticket)

        db.session.commit()

        self.headers = self.auth_header()

    # GET ALL ASSIGNMENTS
    def test_get_all_assignments(self):
        response = self.client.get("/assignments", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # CREATE ASSIGNMENT
    def test_create_assignment_missing_fields(self):
        payload = {"ticket_id": self.ticket.id}  # missing mechanic_id
        response = self.client.post("/assignments", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    # GET SINGLE ASSIGNMENT
    def test_get_assignment_not_found(self):
        response = self.client.get("/assignments/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # UPDATE ASSIGNMENT
    def test_update_assignment_not_found(self):
        payload = {"mechanic_id": self.mechanic.id}
        response = self.client.put("/assignments/999999", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)
