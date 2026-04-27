from .worker import celery
from celery.schedules import crontab
from .models import db, User, ParkingLot, Reservations
from jinja2 import Template
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

import os
import csv


def send_email(email, subject, email_content, attachment=None):

    smtp_server_host = "localhost"
    smtp_port = 1025
    sender_email = "admin@gmail.com"
    sender_password = ""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(email_content, "html"))

    if attachment:
        with open(attachment, "rb") as attachment_content:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_content.read())
            encoders.encode_base64(part)
        
        part.add_header('Content-Disposition', f'attachment; filename = "{os.path.basename(attachment)}')
        msg.attach(part)

    server = smtplib.SMTP(host = smtp_server_host, port =  smtp_port)
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("Mail sent")

def get_html_report(user, reservations, data):
    template = Template(open('report.html').read())
    html_report = template.render(user=user, reservations=reservations, data = data)
    return html_report

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(60.0, daily_reminder.s(), name='daily_reminder at every 60 seconds for testing')

    sender.add_periodic_task(60.0, monthly_report.s(), name='montly report at every 60 seconds for testing')


    sender.add_periodic_task(
        crontab(hour=9, minute=0),
        daily_reminder.s(),
        name='daily_reminder at 9:00am'
    )

    sender.add_periodic_task(
        crontab(hour=10, minute=0, day_of_month='1'),
        monthly_report.s(),
        name='monthly_report at 10:00am on 1st day of month'
    )


@celery.task
def daily_reminder():
    users = User.query.filter_by(role='user').all()
    latest_lot_time = db.session.query(db.func.max(ParkingLot.created_at)).scalar()
    for user in users:
        last_reservation = Reservations.query.filter_by(user_id=user.id).order_by(Reservations.booking_timestamp.desc()).first()

        should_remind = False

        if not last_reservation:
            should_remind = True
        elif latest_lot_time and last_reservation.booking_timestamp < latest_lot_time:
            should_remind = True
        
        if should_remind:
            msg = f"Hey {user.username}, please book a parking spot if required!"
            send_email(email=user.email, subject="Daily Reminder", email_content=msg)

    print("Daily reminder sent to users.")

@celery.task
def monthly_report():
    users = User.query.all()
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    for user in users:
        reservations = Reservations.query.filter(
            Reservations.user_id == user.id,
            Reservations.booking_timestamp >= start_of_month
        ).all()

        if not reservations:
            continue
        
        lot_count = {}
        total_cost = 0.0
        for reservation in reservations:
            lot_id = reservation.lot_id
            if lot_id in lot_count:
                lot_count[lot_id] += 1
            else:
                lot_count[lot_id] = 1
            
            total_cost += reservation.parking_cost
        
        most_used_lot = None
        if lot_count:
            most_used_lot_id = max(lot_count, key=lot_count.get)
            most_used_lot = ParkingLot.query.get(most_used_lot_id)

        
        data = {
            "most_used_lot": most_used_lot,
            "total_cost": total_cost
        }

        html_report = get_html_report(user = user.username, reservations = reservations, data = data)
        send_email(email=user.email, subject="Monthly Report", email_content=html_report)
    
    print("Monthly report sent to all users.")

@celery.task
def data_export(reservation_details, email):

    with open('data_export.csv', 'w', newline = '') as csvfile:
        fieldnames = ['id', 'vehicle_number', 'parking_cost', 'status', 'booking_timestamp', 'parking_timestamp', 'leaving_timestamp', 'lot_id', 'spot_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(reservation_details)
    
    send_email(email=email, subject="Reservation Data Export", email_content="Please find the attached data export.", attachment='data_export.csv')

    return "Data Exported!"