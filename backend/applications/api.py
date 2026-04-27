from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_caching import Cache

cache = Cache()
    
class WelcomeAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
    def get(self):
        return {"message": "Welcome to the Parking Reservation API!"}, 200
    
    def post(self):
        data = request.json
        msg = f"Hello! {data.get('name')}, welcome to the Parking Reservation API!"
        return {"message": msg}, 200