Mechanic Shop API
A RESTful API for managing a mechanic shop system, including users, mechanics, customers, vehicles, service tickets, and assignments.
This project includes full Swagger documentation and a complete unittest test suite.

 Features
User registration, login, and role‑based access
CRUD operations for mechanics, customers, vehicles, tickets, and assignments
Ticket part management
Mechanic ranking
Token‑protected routes
Fully documented with Swagger (OpenAPI 2.0)
Complete test suite using Python’s built‑in unittest
Modular blueprint structure for clean organization

Project Structure
Code
project/
│
├── app.py
├── users/
├── mechanics/
├── customers/
├── vehicles/
├── tickets/
├── assignments/
│
├── swagger_2.0.yaml
│
└── tests/
    ├── test_users.py
    ├── test_mechanics.py
    ├── test_customers.py
    ├── test_vehicles.py
    ├── test_tickets.py
    └── test_assignments.py

Installation & Setup
1. Clone the repository
Code
git clone https://github.com/YourName/your-repo-name
cd your-repo-name
2. Create and activate a virtual environment
Windows

Code
python -m venv venv
venv\Scripts\activate
Mac/Linux

Code
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
Code
pip install -r requirements.txt

 Running the Application
Code
python app.py
The API will run at:

Code
http://127.0.0.1:5000

Swagger Documentation
Swagger UI is available at:

Code
http://127.0.0.1:5000/swagger
The full OpenAPI spec is located in:

Code
swagger_2.0.yaml

Running Tests
All tests are located in the tests/ folder.

Run the entire test suite with:
Windows
Code
python -m unittest discover tests

Mac/Linux
Code
python3 -m unittest discover tests

Technologies Used
Python
Flask
Flask Blueprints
Swagger / OpenAPI 2.0
Unittest
JSON Web Tokens (JWT)

Notes
Some routes require authentication via Authorization: Bearer <token>
Negative tests are included for missing fields, invalid IDs, and unauthorized access
Inventory module is scaffolded but not yet implemented

License
This project is for educational purposes.