from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from .models import db, User
from .api import cache

class LoginAPI(Resource):
    def post(self):
        data = request.json

        if not (data.get('email') and data.get('password')):
            return {"message": "All fields are required."}, 400

        user = User.query.filter_by(email=data.get('email')).first()

        if not user:
            return {"message:" "User not found."}, 400
        
        if user.password != data.get('password'):
            return {"message": "Invalid password."}, 400
        
        token = create_access_token(identity={"user_id": user.id, "role": user.role})
        return {
                "message": f"Welcome back, {user.username}!",
                "token": token,
                "user_name": user.username,
                "user_role": user.role
                }, 200

class RegisterAPI(Resource):
    def post(self):
        data = request.json
        
        if not (data.get('username') and data.get('email') and data.get('password')):
            return {"message": "All fields are required."}, 400
        
        if ("@" not in data.get('email')):
            return {"message": "email should contain @"}, 400

        if len(data.get('email').strip()) < 5:
            return {"message": "email must be atleast 5 chracters long"}, 400
        
        if len(data.get('password').strip()) < 8:
            return {"message": "password must be atleast 8 characters long"}, 400

        user = User.query.filter_by(email=data.get('email')).first()

        if user:
            return {"message": "User already exists."}, 400
        
        new_user = User(username=data.get("username").strip(),
                        email=data.get("email").strip(),
                        password=data.get("password").strip(),
                        role=data.get("role").strip())
        
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "User registered successfully!"}, 201

class ViewUsersAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=30)
    def get(self):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return {"message": "Access Denied."}, 403
        
        users = User.query.filter_by(role='user').all()
        users_json = []
        for user in users:
            users_json.append(user.convert_to_json())
        
        return {"users": users_json}, 200