from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from .models import db, User, ParkingLot, ParkingSpot, Reservations
from datetime import datetime
from .task import data_export

class ReservationAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {"message": "Access Denied."}, 403

        lots = ParkingLot.query.filter_by(is_active=True).all()
        lots_json = []

        for lot in lots:
            lots_json.append({
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pincode": lot.pincode,
                "number_of_spots": lot.number_of_spots,
                "spots": [
                    {
                        "id": spot.id,
                        "status": spot.status,
                        "is_active": spot.is_active
                    } for spot in lot.spots if spot.is_active
                ]
            })
        return {"parking_lots": lots_json}, 200


    @jwt_required()
    def post(self, lot_id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {"message": "Access Denied."}, 403

        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status="Available", is_active=True).first()
        if not spot:
            return {"message": "Spot is not available."}, 404
        
        data = request.json
        if not data.get('vehicle_number'):
            return {"message": "Vehicle Number is required."}, 400

        reservation = Reservations (
            user_id=current_user.get('user_id'),
            spot_id=spot.id,
            lot_id=lot_id,
            booking_timestamp=datetime.now(),
            status="Booked",
            parking_cost = 0.0,
            vehicle_number = data.get('vehicle_number').strip()
        )
        db.session.add(reservation)
        spot.status = "Occupied"
        db.session.commit()

        return {"message": "Reservation successful!"}, 200

class ParkingAPI(Resource):
    @jwt_required()
    def patch(self, reservation_id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {"message": "Access Denied."}, 403
        
        reservation = Reservations.query.filter_by(id=reservation_id, user_id=current_user.get('user_id')).first()
        if not reservation:
            return {"message": "Reservation not found."}, 404
        
        reservation.status = "Parked"
        reservation.parking_timestamp = datetime.now()

        db.session.commit()
        
        return {"message": "Vehicle Parked Successfully"}, 200
    
    @jwt_required()
    def put(self, reservation_id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {"message": "Access Denied."}, 403
        
        reservation = Reservations.query.filter_by(id=reservation_id, user_id=current_user.get('user_id')).first()
        if not reservation:
            return {"message": "Reservation not found."}, 404
        
        if reservation.status != "Parked":
            return {"message": "Vehicle is not parked."}, 400
        
        reservation.status = "Released"
        reservation.leaving_timestamp = datetime.now()
        
        start = reservation.parking_timestamp
        end = reservation.leaving_timestamp
        duration_seconds = (end - start).total_seconds()
        duration_hours = max(1, duration_seconds // 3600)

        lot = reservation.parking_spot.parking_lot
        cost = duration_hours * lot.price

        reservation.parking_cost = cost
        
        spot = ParkingSpot.query.get(reservation.spot_id)
        spot.status = "Available"
        
        db.session.commit()
        
        return {"message": "Vehicle Released Successfully", "cost": reservation.parking_cost}, 200
    
class ViewHistoryAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {"message": "Access Denied."}, 403
        
        reservations = Reservations.query.filter_by(user_id=current_user.get('user_id')).all()

        history_json = []
        for reservation in reservations:
            history_json.append(reservation.convert_to_json())
        
        return {"reservation_history": history_json}, 200

class ReservationDetailsAPI(Resource):
    @jwt_required()
    def get(self, reservation_id):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {"message": "Access Denied."}, 403
        
        reservation = Reservations.query.filter_by(id=reservation_id, user_id=current_user.get('user_id')).first()
        if not reservation:
            return {"message": "Reservation not found."}, 404
        
        return reservation.convert_to_json(), 200

class ExportDataAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {"message": "Access Denied."}, 403
        
        reservations = Reservations.query.filter_by(user_id=current_user.get('user_id')).all()
        user = User.query.get(current_user.get('user_id'))

        if user:
            reservation_details = []
            for reservation in reservations:
                reservation_details.append({"id": reservation.id,
                                            "vehicle_number": reservation.vehicle_number,
                                            "parking_cost": reservation.parking_cost,
                                            "status": reservation.status,
                                            "booking_timestamp": reservation.booking_timestamp.isoformat(),
                                            "parking_timestamp": reservation.parking_timestamp.isoformat(),
                                            "leaving_timestamp": reservation.leaving_timestamp.isoformat(),
                                            "lot_id": reservation.lot_id,
                                            "spot_id": reservation.spot_id})
            data_export(reservation_details, user.email)
            return {"message": "Data export has been initiated, please check your inbox."}, 200

        