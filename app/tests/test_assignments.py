import unittest
from run import app

class TestAssignments(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # GET ALL ASSIGNMENTS
    def test_get_all_assignments(self):
        response = self.client.get("/assignments")
        self.assertEqual(response.status_code, 200)

    # CREATE ASSIGNMENT
    def test_create_assignment_missing_fields(self):
        payload = {
            "ticket_id": 1
            # missing mechanic_id
        }
        response = self.client.post("/assignments", json=payload)
        self.assertIn(response.status_code, [400, 404])

    # GET SINGLE ASSIGNMENT
    def test_get_assignment_not_found(self):
        response = self.client.get("/assignments/999999")
        self.assertEqual(response.status_code, 404)

    # UPDATE ASSIGNMENT
    def test_update_assignment_not_found(self):
        payload = {
            "mechanic_id": 2
        }
        response = self.client.put("/assignments/999999", json=payload)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()