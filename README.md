Mechanic Shop Management API

Project Overview
This is a robust RESTful API built with Flask, Flask-SQLAlchemy, and Flask-Marshmallow designed to manage the operations of a local mechanic shop. It provides full CRUD (Create, Read, Update, Delete) functionality for managing customers, vehicles, service tickets, mechanics, and service assignments.

The application is structured using a modular design to ensure high scalability and separation of concerns, with dedicated files for models, schemas, and individual route modules.

Key Features
The API provides management for five core entities:
Customers: Manage client contact and personal information (unique email validation).
Mechanics: Manage employee data (unique email validation).
Vehicles: Track car details, including VIN (unique validation), and link them to a specific customer (Foreign Key).
Service Tickets: Track open or completed service requests, linked to a specific vehicle (Foreign Key).
Service Assignments: Link service tickets to mechanics, detailing who is working on which job (Foreign Keys).

Prerequisites
Before running this application, you must have the following software installed:
Python 3.8+
MySQL Server (Running locally or accessible via network)
pip (Python package installer)
Postman or curl (For testing API endpoints)
Setup and Installation
Follow these steps to get the project running locally.

1. Clone the Repository (Placeholder)
git clone <repository-url>
cd mechanic-shop-api

2. Create and Activate Virtual Environment
It is highly recommended to use a virtual environment for dependency management.
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

3. Install Dependencies
pip install -r requirements.txt
# (Assuming requirements.txt contains: Flask, Flask-SQLAlchemy, Flask-Marshmallow, python-dotenv, pymysql)