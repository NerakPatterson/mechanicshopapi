Mechanic Shop Management API
A production‑ready, modular REST API built with Flask, SQLAlchemy, and Marshmallow, designed to manage the full workflow of a mechanic shop — including customers, vehicles, service tickets, mechanics, inventory, and user authentication. This project demonstrates clean architecture, scalable design, and professional API engineering practices suitable for real‑world deployment.

Key Features
User Authentication & Roles
JWT‑based login system
Three user roles:
Admin — full access to all resources
Mechanic — limited access (view users, update own info, work on tickets)
Customer — managed through admin
Role‑based route protection using decorators

Customers
Full CRUD
Unique email validation
Linked to vehicles

 Vehicles
Full CRUD
VIN uniqueness enforced
Linked to customers

Mechanics
Full CRUD
Unique email validation
Partial updates supported
Mechanic ranking by ticket count
Linked to service assignments

Service Tickets
Full CRUD
Assign/remove mechanics
Add parts from inventory
Mark tickets as open or closed
Cached GET responses for performance

Inventory
Full CRUD
Link parts to service tickets
Track quantity and pricing

Service Assignments
Link mechanics to tickets
Remove mechanics from tickets
View assignments per ticket

Tech Stack
Component/Technology
Backend Framework: Flask
ORM: SQLAlchemy
Serialization: Marshmallow
Authentication: JWT
Database: MySQL
Migrations: Flask‑Migrate
Caching: Flask‑Caching
Rate Limiting: Flask‑Limiter
Environment Management: python‑dotenv

Installation & Setup
1. Clone the Repository
bash
git clone <repository-url>
cd mechanic-shop-api
2. Create Virtual Environment
bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3. Install Dependencies
bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file:

Code
FLASK_APP=run.py
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost/dbname
JWT_SECRET_KEY=your_secret_key
5. Initialize Database
bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
6. Run the Server
bash
flask run

Project Structure
Code
project_root/
│
├── run.py
├── extensions.py
├── models.py
├── requirements.txt
│
└── app/
    ├── __init__.py
    ├── users/              # Admins, mechanics, customers (auth + CRUD)
    ├── customers/          # Customer routes & schemas
    ├── vehicles/           # Vehicle routes & schemas
    ├── mechanics/          # Mechanic routes & schemas
    ├── service_tickets/    # Ticket routes, parts, status updates
    ├── inventory/          # Parts & stock
    └── assignments/        # Mechanic ↔ Ticket linking