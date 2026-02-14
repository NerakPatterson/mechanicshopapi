from app.tests.base import BaseTestCase
from extensions import db
from models import Vehicle, Customer


class TestVehicles(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Create a customer (vehicles require customer_id)
        self.customer = Customer(
            name="Jane Customer",
            email="jane@customer.com",
            phone="555-1234"
        )
        db.session.add(self.customer)
        db.session.commit()  # ensure self.customer.id exists

        # Create a vehicle for GET/PUT/DELETE tests
        self.vehicle = Vehicle(
            customer_id=self.customer.id,
            make="Toyota",
            model="Camry",
            year=2020,
            vin="123456789ABCDEFG"
        )
        db.session.add(self.vehicle)
        db.session.commit()

        self.headers = self.auth_header()  # admin token

    # GET ALL VEHICLES
    def test_get_all_vehicles(self):
        response = self.client.get("/vehicles", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # CREATE VEHICLE
    def test_create_vehicle_missing_fields(self):
        payload = {"make": "Honda"}  # missing model, year, vin, customer_id
        response = self.client.post("/vehicles", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    # GET SINGLE VEHICLE
    def test_get_vehicle_not_found(self):
        response = self.client.get("/vehicles/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # UPDATE VEHICLE (not found)
    def test_update_vehicle_not_found(self):
        payload = {"make": "Updated Make"}
        response = self.client.put("/vehicles/999999", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # DELETE VEHICLE
    def test_delete_vehicle_not_found(self):
        response = self.client.delete("/vehicles/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)
