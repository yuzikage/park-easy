from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from .models import db, ParkingLot, ParkingSpot
from datetime import datetime


class ParkingLotAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {"message": "Access Denied."}, 403

        lots = ParkingLot.query.filter_by(is_active=True).all()

        lots_json = []
        for lot in lots:
            lots_json.append(lot.convert_to_json())
        return {"parking_lots": lots_json}, 200

    @jwt_required()
    def post(self):

        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {"message": "Access Denied."}, 403
        
        data = request.json
        if not (data.get('prime_location_name') and data.get('price') and data.get('address') and data.get('pincode') and data.get('number_of_spots')):
            return {"message": "All fields are required."}, 400
        
        new_lot = ParkingLot(
            prime_location_name=data.get('prime_location_name').strip(),
            price=data.get('price'),
            address=data.get('address').strip(),
            pincode=data.get('pincode').strip(),
            number_of_spots=data.get('number_of_spots'),
            created_at=datetime.now()
        )

        db.session.add(new_lot)
        db.session.commit()

        for i in range(1, data.get('number_of_spots') + 1):
            spot = ParkingSpot(status="Available", lot_id=new_lot.id)
            db.session.add(spot)
        db.session.commit()

        return {"message": "Parking lot created successfully!"}, 201
    
    @jwt_required()
    def put(self, lot_id):

        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {"message": "Access Denied."}, 403
        
        data = request.json
        
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"message": "Parking lot not found."}, 404
        
        lot.prime_location_name = data.get('prime_location_name').strip() if data.get('prime_location_name') else lot.prime_location_name
        lot.price = data.get('price') if data.get('price') else lot.price
        lot.address = data.get('address').strip() if data.get('address') else lot.address
        lot.pincode = data.get('pincode').strip() if data.get('pincode') else lot.pincode

        new_count = data.get('number_of_spots') if data.get('number_of_spots') else lot.number_of_spots
        current_spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
        active_spots = [spot for spot in current_spots if spot.is_active]

        diff = new_count - len(active_spots)

        if diff > 0:
            for i in range(diff):
                new_spot = ParkingSpot(status="Available", lot_id=lot_id, is_active=True)
                db.session.add(new_spot)
        
        elif diff < 0:
            inactive_count = 0
            for spot in reversed(active_spots):
                if spot.status == "Available":
                    spot.is_active = False
                    inactive_count += 1
                    if inactive_count == abs(diff):
                        break
            
            if inactive_count < abs(diff):
                return {"message": "Can not deactivate spots with active reservations"}, 400

        lot.number_of_spots = new_count
        db.session.commit()

        return {"message": "Parking lot updated successfully!"}, 201
    
    @jwt_required()
    def delete(self, lot_id):

        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {"message": "Access Denied."}, 403
        
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"message": "Parking lot not found."}, 404
        
        booked = ParkingSpot.query.filter(ParkingSpot.lot_id == lot_id, ParkingSpot.status != "Available").first()

        if booked:
            return {"message": "Can not delete a parking lot with booked spots."}, 400
        
        has_history = any(len(spot.reservations) > 0 for spot in lot.spots)

        if has_history:
            lot.is_active = False
            db.session.commit()
            return {"message": "Parking lot deactivated successfully!"}, 201
        else:
            db.session.delete(lot)
            db.session.commit()
            return {"message": "Parking lot deleted permanently!"}, 201
        

class OneLotAPI(Resource):
    @jwt_required()
    def get(self, lot_id):

        lot_json = []
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"message": "Parking lot not found."}, 404
        lot_json.append({
            "id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "price": lot.price,
            "address": lot.address,
            "pincode": lot.pincode,
            "number_of_spots": lot.number_of_spots
        })
        return {"parking_lot": lot_json[0]}, 200