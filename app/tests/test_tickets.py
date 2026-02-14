from app.tests.base import BaseTestCase
from extensions import db
from models import ServiceTicket, Vehicle, Customer, Mechanic, Inventory


class TestTickets(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Create a customer
        self.customer = Customer(
            name="Jane Customer",
            email="jane@customer.com",
            phone="555-1234"
        )
        db.session.add(self.customer)
        db.session.commit()  # ensure self.customer.id exists

        # Create a vehicle linked to the customer
        self.vehicle = Vehicle(
            customer_id=self.customer.id,
            make="Toyota",
            model="Camry",
            year=2020,
            vin="123456789ABCDEFG"
        )
        db.session.add(self.vehicle)
        db.session.commit()  # ensure self.vehicle.id exists

        # Create a mechanic
        self.mechanic = Mechanic(
            name="John Mechanic",
            email="john@shop.com",
            salary=55000
        )
        db.session.add(self.mechanic)

        # Create a part (Inventory item)
        self.part = Inventory(
            name="Oil Filter",
            price=15.99,
            quantity=10
        )
        db.session.add(self.part)
        db.session.commit()

        # Create a ticket linked to the vehicle
        self.ticket = ServiceTicket(
            vehicle_id=self.vehicle.id,
            description="Initial ticket",
            status="open",
            cost=0
        )
        db.session.add(self.ticket)
        db.session.commit()

        self.headers = self.auth_header()  # admin token

    # GET ALL TICKETS
    def test_get_all_tickets(self):
        response = self.client.get("/tickets", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # CREATE TICKET 
    def test_create_ticket_missing_fields(self):
        payload = {"vehicle_id": self.vehicle.id}  # missing description, status, cost
        response = self.client.post("/tickets", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    # GET SINGLE TICKET 
    def test_get_ticket_not_found(self):
        response = self.client.get("/tickets/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # UPDATE TICKET 
    def test_update_ticket_not_found(self):
        payload = {"status": "completed"}
        response = self.client.put("/tickets/999999", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # DELETE TICKET
    def test_delete_ticket_not_found(self):
        response = self.client.delete("/tickets/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # ADD PART TO TICKET 
    def test_add_part_ticket_not_found(self):
        payload = {"part_id": self.part.id, "quantity": 2}
        response = self.client.post("/tickets/999999/add_part", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # ADD PART
    def test_add_part_missing_fields(self):
        payload = {"quantity": 2}  # missing part_id
        response = self.client.post(f"/tickets/{self.ticket.id}/add_part", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    # EDIT MECHANICS ON TICKET
    def test_edit_mechanics_ticket_not_found(self):
        response = self.client.put("/tickets/999999/edit?add_ids=1&remove_ids=2", headers=self.headers)
        self.assertEqual(response.status_code, 404)
