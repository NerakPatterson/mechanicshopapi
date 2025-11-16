Mechanic Shop Management API
A robust RESTful API built with Flask, Flask‑SQLAlchemy, and Flask‑Marshmallow to manage the operations of a local mechanic shop. The system provides full CRUD functionality for customers, vehicles, service tickets, mechanics, and service assignments — all organized with a modular, scalable architecture.

Project Overview
This application demonstrates clean separation of concerns with dedicated modules for:
Models – SQLAlchemy ORM definitions with relationships and constraints
Schemas – Marshmallow serialization for clean JSON responses
Routes – Blueprint‑based modular endpoints for each resource
The design ensures scalability, maintainability, and production‑ready structure.

 Key Features
Customers: Manage client contact and personal information (unique email validation).
Mechanics: Manage employee data with unique email validation.
Vehicles: Track car details, enforce VIN uniqueness, and link vehicles to customers.
Service Tickets: Track open or completed service requests, linked to vehicles.
Service Assignments: Link service tickets to mechanics, defining who is working on which job.

 Prerequisites
Before running this application, ensure you have:
Python 3.8+
MySQL Server (local or network accessible)
pip (Python package installer)
Postman or curl (for testing API endpoints)

 Setup and Installation
1. Clone the Repository
bash
git clone <repository-url>
cd mechanic-shop-api
2. Create and Activate Virtual Environment
bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3. Install Dependencies
bash
pip install -r requirements.txt
(Requirements include Flask, Flask‑SQLAlchemy, Flask‑Marshmallow, Flask‑Migrate, python‑dotenv, PyMySQL, marshmallow‑sqlalchemy.)
4. Configure Environment Variables
Create a .env file in the project root:
Code
FLASK_APP=run.py
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost/dbname
5. Initialize Database
bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
6. Run the Application
bash
flask run

 Project Structure
Code
project_root/
│
├── run.py                # Entry point
├── extensions.py         # Flask extensions (db, ma, migrate)
├── models.py             # SQLAlchemy models
├── requirements.txt      # Dependencies
│
└── app/
    ├── __init__.py       # App factory
    ├── customers/        # Customer routes & schemas
    ├── vehicles/         # Vehicle routes & schemas
    ├── service_tickets/  # Service ticket routes & schemas
    ├── mechanics/        # Mechanic routes & schemas
    └── assignments/      # Service assignment routes & schemas