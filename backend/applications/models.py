from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")

    reservations = db.relationship('Reservations', backref='user', lazy=True)

    def convert_to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }

class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.now())

    spots = db.relationship('ParkingSpot', backref='parking_lot', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<ParkingLot {self.prime_location_name} - {self.price} per hour>"
    
    def convert_to_json(self):
        return {
            "id": self.id,
            "prime_location_name": self.prime_location_name,
            "price": self.price,
            "address": self.address,
            "pincode": self.pincode,
            "number_of_spots": self.number_of_spots,
            "spots": [spot.convert_to_json() for spot in self.spots if spot.is_active],
        }

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default="Available")
    is_active = db.Column(db.Boolean, default=True)

    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    reservations = db.relationship('Reservations', backref='parking_spot', lazy=True)

    current_reservation = db.relationship('Reservations', primaryjoin="and_(Reservations.spot_id==ParkingSpot.id, Reservations.status!='Released')", uselist=False, viewonly=True)

    def convert_to_json(self):
        data = {
            "id": self.id,
            "status": self.status,
            "lot_id": self.lot_id,
            "is_active": self.is_active
        }

        if self.status == "Occupied" and self.current_reservation:
            data["reservation"] = self.current_reservation.convert_to_json()
        else:
            data["reservation"] = None

        return data

class Reservations(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    booking_timestamp = db.Column(db.DateTime, default=datetime.now())
    parking_timestamp = db.Column(db.DateTime, default=datetime.now())
    leaving_timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    parking_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Booked')
    vehicle_number = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)

    def convert_to_json(self):
        return {
            "id": self.id,
            "status": self.status,
            "vehicle_number": self.vehicle_number,
            "user_id": self.user_id,
            "spot_id": self.spot_id,
            "lot_id": self.lot_id,
            "booking_timestamp": self.booking_timestamp.isoformat(),
            "parking_timestamp": self.parking_timestamp.isoformat(),
            "leaving_timestamp": self.leaving_timestamp.isoformat(),
            "parking_cost": self.parking_cost
        }