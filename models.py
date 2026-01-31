from extensions import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

# Junction table: ServiceTicket ↔ Inventory
ticket_parts = db.Table(
    'ticket_parts',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('part_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    vehicles = db.relationship(
        'Vehicle',
        backref='owner',
        cascade="all, delete-orphan",
        lazy=True
    )

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    service_tickets = db.relationship(
        'ServiceTicket',
        backref='vehicle',
        cascade="all, delete-orphan",
        lazy=True
    )

class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    date = db.Column(db.Date, default=func.now(), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Numeric(8, 2), nullable=False)

    assignments = db.relationship(
        'ServiceAssignment',
        backref='ticket',
        cascade="all, delete-orphan",
        lazy=True
    )

    parts = db.relationship(
        'Inventory',
        secondary=ticket_parts,
        back_populates='tickets',
        lazy='subquery'
    )

class Mechanic(db.Model):
    __tablename__ = 'mechanics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    salary = db.Column(db.Numeric(10, 2), nullable=False)

    assignments = db.relationship(
        'ServiceAssignment',
        backref='mechanic',
        cascade="all, delete-orphan",
        lazy=True
    )

class ServiceAssignment(db.Model):
    __tablename__ = 'service_assignment'  # singular to match DB
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # FIXED: match DB schema (VARCHAR(255))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'mechanic', 'customer'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, default=0)

    tickets = db.relationship(
        'ServiceTicket',
        secondary=ticket_parts,
        back_populates='parts',
        lazy='subquery'
    )