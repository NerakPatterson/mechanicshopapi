Mechanic Shop API
A fully documented, tested, and modular Flask REST API for managing a mechanic shop’s operations — including users, customers, vehicles, service tickets, mechanics, assignments, and inventory.

This project demonstrates professional backend engineering practices:
Clean architecture using Flask Blueprints
SQLAlchemy ORM with proper relationships
Marshmallow schemas for validation/serialization
JWT authentication with role‑based access control
Full unit test suite with isolated in‑memory database
Swagger/OpenAPI documentation
Flask‑Migrate for database migrations

Features
Authentication & Authorization
JWT‑based login

Role‑based access control (admin, mechanic, customer)

CRUD Operations
Users
Customers
Vehicles
Service Tickets
Mechanics
Assignments
Inventory
Ticket part management
Mechanic assignment editing

Testing
Full test suite under app/tests/

In‑memory SQLite for clean, isolated runs
Tests cover:
Users
Customers
Vehicles
Mechanics
Tickets
Assignments
Inventory

Documentation
Swagger UI at /swagger

swagger.yaml included for external tools

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
bash
git clone <your-repo-url>
cd mechanic-shop-api
2. Create a virtual environment
bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3. Install dependencies
bash
pip install -r requirements.txt
Environment Variables
Create a .env file:

Code
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
▶Running the App
Option A — Flask CLI
bash
flask run
Option B — Python entrypoint
bash
python run.py
 Running Tests
All tests live under app/tests/.

Run the full suite:
bash
python -m unittest discover app/tests -v
This uses an in‑memory SQLite database, ensuring clean, isolated test runs.

API Documentation (Swagger)
Open your browser to:
Code
/swagger
Or view the raw spec:

Code
app/swagger.yaml
🛠 Tech Stack
Flask 3.x
SQLAlchemy 2.x
Flask‑SQLAlchemy 3.x
Marshmallow / Flask‑Marshmallow
Flask‑Migrate
Flask‑Caching
Flask‑Limiter
PyMySQL (optional for MySQL)
python‑dotenv

Acknowledgments
This project was built as a full backend demonstration of clean architecture, testing discipline, and API design best practices for coding temple.