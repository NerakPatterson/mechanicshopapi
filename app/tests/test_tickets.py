import unittest
from run import app

class TestTickets(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # GET ALL TICKETS
    def test_get_all_tickets(self):
        response = self.client.get("/tickets")
        self.assertEqual(response.status_code, 200)

    # CREATE TICKET
    def test_create_ticket_missing_fields(self):
        payload = {
            "customer_id": 1
            # missing vehicle_id, description
        }
        response = self.client.post("/tickets", json=payload)
        self.assertIn(response.status_code, [400])

    # GET SINGLE TICKET
    def test_get_ticket_not_found(self):
        response = self.client.get("/tickets/999999")
        self.assertEqual(response.status_code, 404)

    # UPDATE TICKET
    def test_update_ticket_not_found(self):
        payload = {
            "status": "completed"
        }
        response = self.client.put("/tickets/999999", json=payload)
        self.assertEqual(response.status_code, 404)

    # DELETE TICKET
    def test_delete_ticket_not_found(self):
        response = self.client.delete("/tickets/999999")
        self.assertEqual(response.status_code, 404)

    # ADD PART TO TICKET
    def test_add_part_ticket_not_found(self):
        payload = {
            "part_id": 1,
            "quantity": 2
        }
        response = self.client.post("/tickets/999999/add_part", json=payload)
        self.assertIn(response.status_code, [404])

    def test_add_part_missing_fields(self):
        payload = {
            "quantity": 2
            # missing part_id
        }
        response = self.client.post("/tickets/1/add_part", json=payload)
        self.assertIn(response.status_code, [400, 404])

    # EDIT MECHANICS ON TICKET
    def test_edit_mechanics_ticket_not_found(self):
        response = self.client.put("/tickets/999999/edit?add_ids=1&remove_ids=2")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()