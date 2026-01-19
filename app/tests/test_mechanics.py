import unittest
from run import app

class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # GET RANKED MECHANICS
    def test_get_ranked_mechanics(self):
        response = self.client.get("/mechanics/ranked")
        self.assertEqual(response.status_code, 200)

    # GET ALL MECHANICS
    def test_get_all_mechanics(self):
        response = self.client.get("/mechanics")
        self.assertEqual(response.status_code, 200)

    # CREATE MECHANIC
    def test_create_mechanic_missing_fields(self):
        payload = {
            "name": "Missing Email"
        }
        response = self.client.post("/mechanics", json=payload)
        self.assertIn(response.status_code, [400, 409])

    # GET SINGLE MECHANIC
    def test_get_mechanic_not_found(self):
        response = self.client.get("/mechanics/999999")
        self.assertEqual(response.status_code, 404)

    # UPDATE MECHANIC
    def test_update_mechanic_not_found(self):
        payload = {
            "name": "Updated Mechanic"
        }
        response = self.client.put("/mechanics/999999", json=payload)
        self.assertEqual(response.status_code, 404)

    # DELETE MECHANIC
    def test_delete_mechanic_not_found(self):
        response = self.client.delete("/mechanics/999999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
