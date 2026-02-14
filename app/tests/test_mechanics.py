from app.tests.base import BaseTestCase
from extensions import db
from models import Mechanic


class TestMechanics(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Create a mechanic for GET/PUT/DELETE tests
        self.mechanic = Mechanic(
            name="John Mechanic",
            email="john_mechanic_test@example.com",
            salary=55000
        )
        db.session.add(self.mechanic)
        db.session.commit()

        self.headers = self.auth_header()  # admin token

    # GET RANKED MECHANICS
    def test_get_ranked_mechanics(self):
        response = self.client.get("/mechanics/ranked", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # GET ALL MECHANICS
    def test_get_all_mechanics(self):
        response = self.client.get("/mechanics", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # CREATE MECHANIC
    def test_create_mechanic_missing_fields(self):
        payload = {"name": "Missing Email"}  # missing email + salary
        response = self.client.post("/mechanics", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    # GET SINGLE MECHANIC
    def test_get_mechanic_not_found(self):
        response = self.client.get("/mechanics/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # UPDATE MECHANIC
    def test_update_mechanic_not_found(self):
        payload = {"name": "Updated Mechanic"}
        response = self.client.put("/mechanics/999999", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # DELETE MECHANIC
    def test_delete_mechanic_not_found(self):
        response = self.client.delete("/mechanics/999999", headers=self.headers)
        self.assertEqual(response.status_code, 404)
