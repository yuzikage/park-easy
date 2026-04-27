from celery import Celery
from flask import current_app as app

def celery_init_app():
    def __call__(self, *args: object, **kwargs: object):
        with app.app_context():
            return self.run(*args, **kwargs)

    celery_app = Celery()

    return celery_app

celery = celery_init_app()