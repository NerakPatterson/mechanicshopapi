Mechanic Shop API
A fully documented, tested, and modular Flask REST API for managing a mechanic shop’s operations — including users, customers, vehicles, service tickets, mechanics, assignments, and inventory.

Features
User registration & login (JWT-based)
Role-based access control (admin, mechanic, customer)
CRUD operations for:
Users
Customers
Vehicles
Service Tickets
Mechanics
Assignments
Inventory

Swagger/OpenAPI documentation
Full unit test suite with isolated in-memory database
Clean project structure using Flask blueprints
Marshmallow serialization
SQLAlchemy ORM
Flask-Migrate migrations

Project Structure
Code
app/
    users/
    customers/
    mechanics/
    vehicles/
    tickets/
    assignments/
    inventory/
    tests/
        base.py
        test_users.py
        test_customers.py
        test_mechanics.py
        test_vehicles.py
        test_tickets.py
        test_assignments.py
        test_inventory.py
    models.py
    extensions.py
    swagger.yaml
run.py
README.md

Installation
1. Clone the repository
Code
git clone <your-repo-url>
cd mechanic-shop-api
2. Create a virtual environment
Code
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3. Install dependencies
Code
pip install -r requirements.txt
Environment Variables
Create a .env file:

Code
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db

Running the App
Code
flask run
Or:
Code
python run.py

Running Tests
Your tests now live under app/tests/.
Run the full suite:
Code
python -m unittest discover app/tests
This uses an in-memory SQLite database for clean, isolated test runs.

API Documentation (Swagger)
Your full API documentation is available at:
Code
/swagger
Or open the swagger.yaml file directly.

Tech Stack
Flask 3.x
SQLAlchemy 2.x
Flask‑SQLAlchemy 3.x
Marshmallow / Flask‑Marshmallow
Flask‑Migrate
PyMySQL (optional for MySQL)
python‑dotenv