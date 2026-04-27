from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from .models import ParkingLot, Reservations
from collections import defaultdict
from .api import cache

class UserSummaryAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'user':
            return {"message": "Access Denied."}, 403

        user_id = current_user.get('user_id')
        reservations = Reservations.query.filter_by(user_id=user_id).all()

        status_count = defaultdict(int)
        location_count = defaultdict(int)

        for reservation in reservations:

            status_count[reservation.status] += 1

            if reservation.lot_id and reservation.spot_id:
                lot = ParkingLot.query.get(reservation.lot_id)
                if lot:
                    location_count[lot.prime_location_name] += 1

        return {
            "status_summary": status_count,
            "location_summary": location_count
        }, 200
    
class AdminSummaryAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {"message": "Access Denied."}, 403

        lots = ParkingLot.query.all()
        total_spots = sum(lot.number_of_spots for lot in lots if lot.is_active)
        occupied_spots = sum(spot.status == "Occupied" for lot in lots for spot in lot.spots if spot.is_active)
        available_spots = total_spots - occupied_spots

        bookings_count = defaultdict(int)
        reservations = Reservations.query.all()
        for reservation in reservations:
            if reservation.lot_id:
                bookings_count[reservation.lot_id] += 1
        
        lots = ParkingLot.query.all()
        lot_names = {lot.id: lot.prime_location_name for lot in lots}

        bookings_summary = {
            lot_names[lot_id]: count for lot_id, count in bookings_count.items()
        }

        return {
            "occupancy_summary":{
                "Total Spots": total_spots,
                "Occupied Spots": occupied_spots,
                "Available Spots": available_spots
            },
            "bookings_summary": bookings_summary
        }, 200