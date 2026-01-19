import unittest
from run import app

class TestVehicles(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # GET ALL VEHICLES
    def test_get_all_vehicles(self):
        response = self.client.get("/vehicles")
        self.assertEqual(response.status_code, 200)

    # CREATE VEHICLE
    def test_create_vehicle_missing_fields(self):
        payload = {
            "make": "Honda"
            # missing model, year, vin, customer_id
        }
        response = self.client.post("/vehicles", json=payload)
        self.assertIn(response.status_code, [400, 409])

    # GET SINGLE VEHICLE
    def test_get_vehicle_not_found(self):
        response = self.client.get("/vehicles/999999")
        self.assertEqual(response.status_code, 404)

    # UPDATE VEHICLE
    def test_update_vehicle_not_found(self):
        payload = {
            "make": "Updated Make"
        }
        response = self.client.put("/vehicles/999999", json=payload)
        self.assertEqual(response.status_code, 404)

    # DELETE VEHICLE
    def test_delete_vehicle_not_found(self):
        response = self.client.delete("/vehicles/999999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
