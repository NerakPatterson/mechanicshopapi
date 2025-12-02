from extensions import db
from sqlalchemy.sql import func

# Junction table: ServiceTicket ↔ Inventory
service_ticket_inventory = db.Table(
    'service_ticket_inventory',
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(255), nullable=False)

    vehicles = db.relationship(
        'Vehicle',
        backref='owner',
        cascade="all, delete-orphan",
        lazy=True
    )

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vin = db.Column(db.String(17), nullable=False, unique=True)
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
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    date = db.Column(db.DateTime, default=func.now(), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Numeric(8, 2), nullable=False)

    service_assignments = db.relationship(
        'ServiceAssignment',
        backref='ticket',
        cascade="all, delete-orphan",
        lazy=True
    )

    # Many-to-many: tickets ↔ inventory parts
    inventory_parts = db.relationship(
        'Inventory',
        secondary=service_ticket_inventory,
        back_populates='tickets',
        lazy='subquery'
    )

class Mechanic(db.Model):
    __tablename__ = 'mechanics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    salary = db.Column(db.Numeric(10, 2), nullable=False)

    service_assignments = db.relationship(
        'ServiceAssignment',
        backref='mechanic',
        cascade="all, delete-orphan",
        lazy=True
    )

class ServiceAssignment(db.Model):
    __tablename__ = 'service_assignments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Many-to-many: inventory parts ↔ tickets
    tickets = db.relationship(
        'ServiceTicket',
        secondary=service_ticket_inventory,
        back_populates='inventory_parts',
        lazy='subquery'
    )