from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from applications.models import db, User
from applications.api import WelcomeAPI, cache
from applications.auth_api import LoginAPI, RegisterAPI, ViewUsersAPI
from applications.parking_lot_api import ParkingLotAPI, OneLotAPI
from applications.reservation_api import ReservationAPI, ParkingAPI, ViewHistoryAPI, ReservationDetailsAPI, ExportDataAPI

from applications.summary_api import UserSummaryAPI, AdminSummaryAPI

from applications.worker import celery
from applications.task import *

from datetime import timedelta
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["JWT_SECRET_KEY"] = "project-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 0
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1',
    timezone='Asia/Kolkata'
)

db.init_app(app)
cache.init_app(app)
api = Api(app)
jwt = JWTManager(app)
app.app_context().push()

def add_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(username="admin", email="admin@gmail.com", password="admin", role="admin")
        db.session.add(admin)
        db.session.commit()
        return "Admin added successfully."

@app.route('/test-cache')
@cache.cached(timeout=10)
def test_cache():
    time.sleep(10)
    return f"Testing is working {time.localtime()}"

api.add_resource(WelcomeAPI, '/api/welcome')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(RegisterAPI, '/api/register')

api.add_resource(ParkingLotAPI, '/api/parking-lot', '/api/parking-lot/<int:lot_id>')
api.add_resource(OneLotAPI, '/api/a-parking-lot/<int:lot_id>')

api.add_resource(ViewUsersAPI, '/api/users')

api.add_resource(ReservationAPI, '/api/view-parking-lots/', '/api/parking-lot/<int:lot_id>/reserve')
api.add_resource(ParkingAPI, '/api/parking-lot/reservation/<int:reservation_id>')
api.add_resource(ViewHistoryAPI, '/api/history')
api.add_resource(ReservationDetailsAPI, '/api/reservation-details/<int:reservation_id>')

api.add_resource(ExportDataAPI, '/api/export')

api.add_resource(UserSummaryAPI, '/api/user-summary')
api.add_resource(AdminSummaryAPI, '/api/admin-summary')

if __name__ == '__main__':
    db.create_all()
    add_admin()
    app.run(debug=True)